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
from typing import Any, Dict, Optional
from typing import Any, Dict, Optional

from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext
from google.adk.tools import BaseTool, ToolContext
from google.adk.tools.bigquery import BigQueryToolset, BigQueryCredentialsConfig
from google.adk.tools.bigquery.config import BigQueryToolConfig, WriteMode
from google.genai import types
import google.auth
from .prompts import return_instructions_bigquery

# Initialize the tools to use the application default credentials.
application_default_credentials, _ = google.auth.default()
credentials_config = BigQueryCredentialsConfig(
    credentials=application_default_credentials
)

def setup_before_agent_call(callback_context: CallbackContext) -> None:
    """Setup the agent."""
    return




logger = logging.getLogger(__name__)

def store_results_in_context(
    tool: BaseTool, args: Dict[str, Any], tool_context: ToolContext, tool_response: Dict
) -> Optional[Dict]:
    """
    Callback/hook that stores successful query results in tool_context.state.

    - Never throws if tool_response shape differs (prevents UI/session crashes).
    - Stores rows if present; otherwise stores the full response for debugging.
    """

    # Only handle the BigQuery SQL execution tool
    if tool.name != "execute_sql":
        return None

    # Defensive: tool_response might not be a dict in some edge cases
    if not isinstance(tool_response, dict):
        tool_context.state["query_result"] = tool_response
        return None

    status = tool_response.get("status")

    # If status isn't present, don't crash—store raw response so you can inspect it
    if status is None:
        tool_context.state["query_result"] = tool_response
        logger.warning("execute_sql tool_response missing 'status'. Stored raw response.")
        return None

    # Only store results on success
    if status == "SUCCESS":
        rows = tool_response.get("rows")

        # If rows aren't present, store raw response and log keys for debugging
        if rows is None:
            tool_context.state["query_result"] = tool_response
            logger.warning(
                "execute_sql SUCCESS response missing 'rows'. Keys=%s",
                list(tool_response.keys())
            )
            # Optional: log a short preview (won't blow up on non-serializable types)
            try:
                logger.info(
                    "execute_sql response preview: %s",
                    json.dumps(tool_response, default=str)[:1500]
                )
            except Exception:
                pass
            return None

        # Normal path: store rows
        tool_context.state["query_result"] = rows
        return None

    # Non-success: store error payload (useful for agent + UI debugging)
    tool_context.state["query_result"] = tool_response
    return None



bigquery_tool_filter = ['list_dataset_ids','get_dataset_info','list_table_ids','get_table_info','execute_sql']
bigquery_tool_config = BigQueryToolConfig(
    write_mode=WriteMode.BLOCKED,
    max_query_result_rows=80
)
credentials_config = BigQueryCredentialsConfig(
    credentials=application_default_credentials
)

bigquery_toolset = BigQueryToolset(
    credentials_config=credentials_config,
    tool_filter=bigquery_tool_filter,
    bigquery_tool_config=bigquery_tool_config
)

database_agent = Agent(
    model=os.getenv("ROOT_AGENT_MODEL"),
    name="database_agent",
    instruction=return_instructions_bigquery(),
    tools=[
        bigquery_toolset,
    ],
    before_agent_callback=setup_before_agent_call,
    after_tool_callback=store_results_in_context,
    generate_content_config=types.GenerateContentConfig(temperature=0.01),
)