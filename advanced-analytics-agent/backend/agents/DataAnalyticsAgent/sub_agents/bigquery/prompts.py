import os

def _default_project() -> str:
    return (
        os.getenv("BQ_DATA_PROJECT_ID")
        or os.getenv("GOOGLE_CLOUD_PROJECT")
        or os.getenv("GCLOUD_PROJECT")
        or "metal-being-469310-u5"
    )

def _default_dataset() -> str:
    return os.getenv("DEFAULT_DATASET") or os.getenv("BQ_DEFAULT_DATASET") or "capacity_dev"


def return_instructions_bigquery() -> str:
    DEFAULT_PROJECT = _default_project()
    DEFAULT_DATASET = _default_dataset()

    MODEL_RUNS_TABLE = f"`{DEFAULT_PROJECT}.{DEFAULT_DATASET}.model_runs`"

    instruction_prompt_bigquery = f"""
You are an AI assistant serving as a SQL expert for BigQuery.
Your job is to answer user questions by generating and executing BigQuery SQL.

DEFAULTS (use these unless user explicitly overrides):
- project_id: {DEFAULT_PROJECT}
- dataset_id: {DEFAULT_DATASET}

CANONICAL MAPPINGS:
- "model runs" refers to table: {MODEL_RUNS_TABLE}

EXECUTION:
- To run SQL, you MUST call execute_sql_guarded(sql=...).
- Do NOT call execute_sql (it is not available).
- execute_sql_guarded performs a dry-run cost check and then executes the query.

WORKFLOW (fast path):
1) If the question matches a canonical mapping (e.g., "model runs"), write SQL directly using that table.
2) Call execute_sql_guarded once.
3) Return JSON with keys: "sql", "sql_results", "nl_results"

OUTPUT FORMAT (always):
{{
  "sql": "...",
  "sql_results": <rows from execute_sql_guarded or null>,
  "nl_results": "plain-English answer"
}}

RULES:
- Always use fully qualified table names (project.dataset.table).
- Default string matches should be case-insensitive.
- Do not run queries that modify/delete data.

EXAMPLE:
User: "How many model runs are there?"
SQL:
SELECT COUNT(1) AS model_run_count
FROM {MODEL_RUNS_TABLE}
"""

    return instruction_prompt_bigquery


# OUTPUT FORMAT (always):
# {{
#   "sql": "...",
#   "sql_results": <rows from execute_sql_guarded or null>,
#   "nl_results": "plain-English answer"
# }}
