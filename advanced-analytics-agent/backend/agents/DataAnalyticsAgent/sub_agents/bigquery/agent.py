# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Database Agent: get data from database (BigQuery) using NL2SQL."""

import os
import json
import logging
import datetime
import decimal
from typing import Any, Dict, Optional

from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext
from google.adk.tools import BaseTool, ToolContext
from google.adk.tools.bigquery import BigQueryToolset, BigQueryCredentialsConfig
from google.adk.tools.bigquery.config import BigQueryToolConfig, WriteMode
from google.genai import types
import google.auth

from .prompts import return_instructions_bigquery
from .execute_sql_guarded import execute_sql_guarded


logger = logging.getLogger(__name__)

# Initialize the tools to use the application default credentials.
application_default_credentials, _ = google.auth.default()
credentials_config = BigQueryCredentialsConfig(credentials=application_default_credentials)


def setup_before_agent_call(callback_context: CallbackContext) -> None:
    """Setup the agent."""
    return


def make_json_safe(obj: Any) -> Any:
    """
    Recursively convert objects to JSON-serializable equivalents.
    This is critical because ADK persists tool_context.state via json.dumps(...).
    """
    if obj is None:
        return None

    # BigQuery / Python common non-JSON types
    if isinstance(obj, (datetime.datetime, datetime.date, datetime.time)):
        return obj.isoformat()

    if isinstance(obj, decimal.Decimal):
        return float(obj)

    # Containers
    if isinstance(obj, dict):
        return {str(k): make_json_safe(v) for k, v in obj.items()}

    if isinstance(obj, (list, tuple, set)):
        return [make_json_safe(v) for v in obj]

    # JSON primitives
    if isinstance(obj, (str, int, float, bool)):
        return obj

    # Last resort: stringify
    return str(obj)


def store_results_in_context(
    tool: BaseTool, args: Dict[str, Any], tool_context: ToolContext, tool_response: Any
) -> Optional[Dict]:
    """
    Callback/hook that stores successful query results in tool_context.state.

    IMPORTANT: Anything written to tool_context.state must be JSON-serializable
    because ADK persists session deltas via json.dumps(...).
    """

    # Only handle SQL execution tools (ADK may name function tools by __name__)
    if tool.name not in ("execute_sql", "execute_sql_guarded"):
        return None

    # Always sanitize before storing anything in state
    safe_response = make_json_safe(tool_response)

    # Defensive: safe_response might not be a dict (e.g. string/None)
    if not isinstance(safe_response, dict):
        tool_context.state["last_bq_tool_response"] = safe_response
        tool_context.state["last_bq_status"] = "UNKNOWN"
        return None

    status = safe_response.get("status")

    # Store minimal, stable fields (keeps session delta small and avoids surprises)
    tool_context.state["last_sql"] = safe_response.get("sql")
    tool_context.state["last_schema"] = safe_response.get("schema")
    tool_context.state["last_bq_status"] = status

    if status == "SUCCESS":
        rows = safe_response.get("rows")

        if rows is None:
            # Store full safe response for debugging
            tool_context.state["last_bq_tool_response"] = safe_response
            logger.warning(
                "%s SUCCESS response missing 'rows'. Keys=%s",
                tool.name,
                list(safe_response.keys()),
            )
            try:
                logger.info(
                    "%s response preview: %s",
                    tool.name,
                    json.dumps(safe_response, default=str)[:1500],
                )
            except Exception:
                pass
            return None

        # Store only rows (already JSON-safe)
        tool_context.state["last_rows"] = rows[:200]
        # Keep backwards compatibility if other code expects query_result
        tool_context.state["query_result"] = rows
        return None

    # Non-success: store safe error payload for debugging
    tool_context.state["last_bq_tool_response"] = safe_response
    tool_context.state["query_result"] = safe_response
    return None


# --- BigQuery toolset configuration ---
bigquery_tool_filter = ["get_dataset_info", "get_table_info"]

bigquery_tool_config = BigQueryToolConfig(
    write_mode=WriteMode.BLOCKED,
    max_query_result_rows=80,
)

bigquery_toolset = BigQueryToolset(
    credentials_config=credentials_config,
    tool_filter=bigquery_tool_filter,
    bigquery_tool_config=bigquery_tool_config,
)

execute_sql_guarded_tool = execute_sql_guarded

database_agent = Agent(
    model=os.getenv("ROOT_AGENT_MODEL"),
    name="database_agent",
    instruction=return_instructions_bigquery(),
    tools=[bigquery_toolset, execute_sql_guarded_tool],
    before_agent_callback=setup_before_agent_call,
    after_tool_callback=store_results_in_context,
    generate_content_config=types.GenerateContentConfig(temperature=0.01),
)
