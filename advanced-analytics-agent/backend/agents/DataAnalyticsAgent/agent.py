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

"""Top level agent for data agent multi-agents.

-- it get data from database (e.g., BQ) using NL2SQL
-- then, it use NL2Py to do further data analysis as needed
"""
import os
from datetime import date

from google.genai import types

from google.adk.agents import Agent, SequentialAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.tools import load_artifacts 
from google.adk.tools.retrieval.vertex_ai_rag_retrieval import VertexAiRagRetrieval
from vertexai import rag
from .prompts import return_instructions_root, return_instructions_tester
from vertexai.preview import reasoning_engines
from .tools import call_db_agent, call_alert_agent, call_knowledgebase_agent, call_localfile_agent, call_code_executor_agent
from google.adk.tools.mcp_tool import MCPToolset , StdioConnectionParams
from mcp import StdioServerParameters
from .sub_agents import db_agent

date_today = date.today()



def setup_before_agent_call(callback_context: CallbackContext):
    """Setup the agent."""

    # setting up database settings in session.state
    if "database_settings" not in callback_context.state:
        db_settings = dict()
        db_settings["use_database"] = "BigQuery"
        callback_context.state["all_db_settings"] = db_settings

    # setting up schema in instruction
    if callback_context.state["all_db_settings"]["use_database"] == "BigQuery":
        # callback_context.state["database_settings"] = get_bq_database_settings()
        # schema = callback_context.state["database_settings"]["bq_schema_and_samples"]
         callback_context._invocation_context.agent.instruction = return_instructions_root()


# ask_vertex_retrieval = VertexAiRagRetrieval(
#     name='retrieve_rag_documents',
#     description=(
#         'Use this tool to retrieve documentation and reference materials for the question from the RAG corpus,'
#     ),
#     rag_resources=[
#         rag.RagResource(
#             # please fill in your own rag corpus
#             # here is a sample rag corpus for testing purpose
#             # e.g. projects/123/locations/us-central1/ragCorpora/456
#             rag_corpus="projects/ddaastransformdev/locations/us-central1/ragCorpora/5764607523034234880"
#         )
#     ],
#     similarity_top_k=10,
#     vector_distance_threshold=0.6,
# )

# rag_agent = Agent(
#     model='gemini-2.5-flash',
#     name='ask_rag_agent',
#     instruction="""   
#         you are an knowledge retrieval tool that will fetch the results from RAG vector store, do not summarize or change the content
        
#         Include original request in the output

#         Citation Format Instructions:
 
#         When you provide an answer, you must also add one or more citations **at the end** of
#         your answer. If your answer is derived from only one retrieved chunk,
#         include exactly one citation. If your answer uses multiple chunks
#         from different files, provide multiple citations. If two or more
#         chunks came from the same file, cite that file only once.

#         **How to cite:**
#         - Use the retrieved chunk's `title` to reconstruct the reference.
#         - Include the document title and section if available.
#         - For web resources, include the full URL when available.
 
        
#         """,
#     tools=[
#         ask_vertex_retrieval,
#     ],

#     generate_content_config=types.GenerateContentConfig(temperature=0.01),
# )



# tester_agent = Agent(
#     model=os.getenv("ROOT_AGENT_MODEL"),
#     name="TestAgent",
#     instruction=return_instructions_tester(),
    
#     tools=[
#          call_knowledgebase_agent,
#          call_db_agent,
#          call_localfile_agent,
#          call_code_executor_agent],
#          #

#     global_instruction=(
#         f"""
#         You are a Tester that will validate files or queries mentioned in the request
#         Todays date: {date_today}
#         """
#     ),
#     before_agent_callback=setup_before_agent_call,
#     generate_content_config=types.GenerateContentConfig(temperature=0.01),
# )

# mcptools = MCPToolset(connection_params=StdioConnectionParams(
#         server_params = StdioServerParameters(
#         command='npx',
#         args=[
#             "-y", "mcp-remote", "https://mcp.atlassian.com/v1/sse"
#         ],
#         env={}
#     )))


# mcp_atlassian_agent = Agent(
#  model=os.getenv("ROOT_AGENT_MODEL"),
#     name="atlassian_agent",
#     instruction="""you are a atlassian agent that has access to confluence and jira""",
#     tools=[mcptools],
#     generate_content_config=types.GenerateContentConfig(temperature=0.01, top_p = 0.5),
# )

dev_agent = Agent(
    model=os.getenv("ROOT_AGENT_MODEL"),
    name="SQLAgent",
    instruction=return_instructions_root(),
    
    tools=[
         #call_knowledgebase_agent,
         call_db_agent,
         #call_localfile_agent,
         call_code_executor_agent
         ],
         #

    global_instruction=(
        f"""
        You are a Data Science and Data Analytics Multi Agent System.
        Todays date: {date_today}
        """
    ),
    before_agent_callback=setup_before_agent_call,
    generate_content_config=types.GenerateContentConfig(temperature=0.01, top_p = 0.5),
)


root_agent = db_agent


# root_agent = SequentialAgent(
#     name="DataAnalyticsAgent",
#     sub_agents=[ dev_agent],
#     description="Executes a sequence to retrieve information and process request",
#     # The agents will run in the order provided: Writer -> Reviewer -> Refactorer
# )