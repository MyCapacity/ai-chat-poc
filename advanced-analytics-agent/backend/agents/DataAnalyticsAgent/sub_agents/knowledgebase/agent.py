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
from google.adk.tools.bigquery import BigQueryToolset, BigQueryCredentialsConfig
from google.adk.tools.bigquery.config import BigQueryToolConfig, WriteMode
from google.genai import types
import google.auth
from .prompts import return_instructions_knowledgebase
from vertexai import rag
from vertexai.preview import reasoning_engines
from google.adk.tools.retrieval.vertex_ai_rag_retrieval import VertexAiRagRetrieval

ask_vertex_retrieval = VertexAiRagRetrieval(
    name='retrieve_rag_documents',
    description=(
        'Use this tool to retrieve documentation and reference materials for the question from the RAG corpus,'
    ),
    rag_resources=[
        rag.RagResource(
            # please fill in your own rag corpus
            # here is a sample rag corpus for testing purpose
            # e.g. projects/123/locations/us-central1/ragCorpora/456
            rag_corpus=os.environ.get("ANALYTICS_RAG_CORPUS_NAME")
        )
    ],
    similarity_top_k=10,
    vector_distance_threshold=0.6,
)


def setup_before_agent_call(callback_context: CallbackContext) -> None:
    """Setup the agent."""
    return


def store_results_in_context(
    tool: BaseTool, args: Dict[str, Any], tool_context: ToolContext, tool_response: Dict
) -> Optional[Dict]:

    # We are setting a state for the data science agent to be able to use the sql
    # query results as context 
    if tool.name == "knolwedgebase":
        if tool_response["status"] == "SUCCESS":
            tool_context.state["result"] = tool_response

    return None


knowledgebase_agent = Agent(
    model=os.getenv("ROOT_AGENT_MODEL"),
    name="database_agent",
    instruction=return_instructions_knowledgebase(),
    tools=[
        ask_vertex_retrieval
    ],
    before_agent_callback=setup_before_agent_call,
    after_tool_callback=store_results_in_context,
    generate_content_config=types.GenerateContentConfig(temperature=0.01,top_p=0.5 ),
)