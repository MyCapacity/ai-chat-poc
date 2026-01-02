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

from typing import Any, Dict, Optional

from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext
from google.adk.tools import BaseTool, ToolContext
from google.genai import types
import google.auth
from .prompts import return_instructions_localFile
from .FileTool import FileTool

def setup_before_agent_call(callback_context: CallbackContext) -> None:
    """Setup the agent."""
    return


def store_results_in_context(
    tool: BaseTool, args: Dict[str, Any], tool_context: ToolContext, tool_response: Dict
) -> Optional[Dict]:
    tool_context.state["response"] = tool_response

    return None


file_tool_instance = FileTool(base_path="c://work//crown//ddaas-ai-poc//generated")


localfile_agent = Agent(
    model=os.getenv("ROOT_AGENT_MODEL"),
    name="localfile_agent",
    instruction=return_instructions_localFile(),
    tools=[
        file_tool_instance.read, file_tool_instance.write, file_tool_instance.list
    ],
    before_agent_callback=setup_before_agent_call,
    after_tool_callback=store_results_in_context,
    generate_content_config=types.GenerateContentConfig(temperature=0.01),
)