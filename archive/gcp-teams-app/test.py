
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    AgentEventHandler,
    RunStep,
    RunStepDeltaChunk,
    ThreadMessage,
    ThreadRun,
    MessageDeltaChunk,
    BingGroundingTool,
    FilePurpose,
    FileSearchTool,
    FunctionTool,
    ToolSet,
    SubmitToolOutputsAction,
    RequiredFunctionToolCall,
    MessageTextContent,
    ToolOutput
)

credentials = DefaultAzureCredential()

client = AIProjectClient.from_connection_string( credential = credentials, conn_str ="australiaeast.api.azureml.ms;e5b99aab-c321-43ec-bb33-e46e45180865;ddaas-ai-poc;ddaas-ai-poc-std-myyy")

all_vector_stores = client.agents.list_vector_stores().data


for x in all_vector_stores:
    print(x)
    #if(x.id != "vs_KUMlc94nUtHx88QpNJ8xC4Lx"):
        #client.agents.delete_vector_store(x.id)
    #    print(f"deleting... {x.id}")