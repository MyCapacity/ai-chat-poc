from __future__ import annotations
import os
import time
from typing import Any, Dict, List, Optional

from google.cloud import bigquery


import datetime
import decimal
from typing import Any

def make_json_safe(obj: Any) -> Any:
    if obj is None:
        return None

    if isinstance(obj, (datetime.datetime, datetime.date, datetime.time)):
        return obj.isoformat()

    if isinstance(obj, decimal.Decimal):
        return float(obj)

    if isinstance(obj, dict):
        return {str(k): make_json_safe(v) for k, v in obj.items()}

    if isinstance(obj, (list, tuple, set)):
        return [make_json_safe(v) for v in obj]

    if isinstance(obj, (str, int, float, bool)):
        return obj

    # last-resort fallback
    return str(obj)



def _get_default_project() -> Optional[str]:
    # Prefer your existing envs (these show up in your repo)
    return (
        os.getenv("BQ_DATA_PROJECT_ID")
        or os.getenv("GOOGLE_CLOUD_PROJECT")
        or os.getenv("GCLOUD_PROJECT")
    )


def _get_default_location() -> str:
    return os.getenv("BQ_LOCATION") or "australia-southeast1"


def execute_sql_guarded(
    sql: str,
    project_id: Optional[str] = None,
    location: Optional[str] = None,
    max_gb_processed: float = 50.0,
    max_rows: int = 200,
    timeout_s: int = 30,
    use_query_cache: bool = True,
) -> Dict[str, Any]:
    """
    Executes a BigQuery query with built-in cost guardrails:
      1) dry run to estimate bytes
      2) reject if estimated bytes > max_gb_processed
      3) execute real query and return rows

    Returns a dict designed for LLM consumption.
    """
    if not sql or not isinstance(sql, str):
        raise ValueError("sql must be a non-empty string")

    project_id = project_id or _get_default_project()
    location = location or _get_default_location()

    if not project_id:
        raise ValueError(
            "No project_id provided and no default project env var found "
            "(set BQ_DATA_PROJECT_ID or GOOGLE_CLOUD_PROJECT)."
        )

    client = bigquery.Client(project=project_id, location=location)

    # -------- 1) DRY RUN --------
    dry_config = bigquery.QueryJobConfig(
        dry_run=False,
        use_query_cache=use_query_cache,
        use_legacy_sql=False,
    )

    t0 = time.time()
    dry_job = client.query(sql, job_config=dry_config, location=location)
    # For dry_run, total_bytes_processed is populated without running the query
    bytes_processed = int(getattr(dry_job, "total_bytes_processed", 0) or 0)
    gb_processed = bytes_processed / (1024**3)

    if gb_processed > max_gb_processed:
        return {
            "status": "REJECTED_TOO_LARGE",
            "reason": f"Estimated bytes processed {gb_processed:.2f}GB exceeds limit {max_gb_processed:.2f}GB",
            "estimated_bytes_processed": bytes_processed,
            "estimated_gb_processed": gb_processed,
            "sql": sql,
            "project_id": project_id,
            "location": location,
            "elapsed_ms": int((time.time() - t0) * 1000),
        }

    # -------- 2) REAL EXECUTION --------
    exec_config = bigquery.QueryJobConfig(
        dry_run=False,
        use_query_cache=use_query_cache,
        use_legacy_sql=False,
    )
    job = client.query(sql, job_config=exec_config, location=location)

    # Wait for results (timeout applies to .result)
    result_iter = job.result(timeout=timeout_s)

    # -------- 3) MATERIALIZE ROWS --------
    # Keep payload small: cap max_rows
    rows: List[Dict[str, Any]] = []
    schema_fields = [f.name for f in result_iter.schema] if result_iter.schema else []

    for i, row in enumerate(result_iter):
        if i >= max_rows:
            break
        # Row supports dict(row) in most cases; explicit mapping is safer:
        rows.append({k: make_json_safe(row.get(k)) for k in schema_fields})


    return make_json_safe({
        "status": "SUCCESS",
        "sql": sql,
        "project_id": project_id,
        "location": location,
        "estimated_bytes_processed": bytes_processed,
        "estimated_gb_processed": gb_processed,
        "job_id": job.job_id,
        "rows": rows,
        "schema": schema_fields,
        "row_count_returned": len(rows),
        "elapsed_ms": int((time.time() - t0) * 1000),
        "note": f"Returned up to {max_rows} rows",
    })
