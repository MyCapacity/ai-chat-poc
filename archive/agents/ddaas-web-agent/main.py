import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.projects.telemetry import trace_function
from azure.ai.projects.models import FunctionTool, ToolSet, FilePurpose, FileSearchTool, MessageTextContent, AzureFunctionTool,AzureFunctionStorageQueue,  CodeInterpreterTool, MessageImageFileContent
import glob

# Instrument AI Inference API 

# Create an Azure AI Client from a connection string
project_client = AIProjectClient.from_connection_string(
    credential=DefaultAzureCredential(),
    conn_str="australiaeast.api.azureml.ms;e5b99aab-c321-43ec-bb33-e46e45180865;DDaaS-AI-POC;ddaas-ai-poc-std-myyy",
)

def ConfigureAgent() :
    vector_store_id = "vs_KUMlc94nUtHx88QpNJ8xC4Lx"
    """
    stores = project_client.agents.list_vector_stores()
    print(stores)
    for store in stores.data:
        print(store)
        if store.name == "BqVectorStore" and store.id != vector_store_id:
            project_client.agents.delete_vector_store(vector_store_id = store.id)
            print(f"deleted {store}")
    """
    # Create vector store
    vector_store = project_client.agents.get_vector_store(vector_store_id = vector_store_id)

    # Clear existing files in vector store
    existingFiles = project_client.agents.list_vector_store_files(vector_store_id=vector_store.id)
    for f in existingFiles.data:
        print (f"removing {f}")
        project_client.agents.delete_vector_store_file(vector_store_id=vector_store.id, file_id=f.id)

    # Upload and process all files from data directory
    data_dir = './data'
    file_ids = []
    for file_path in glob.glob(os.path.join(data_dir, '*.*')):
        print(f"Uploading file: {file_path}")
        file = project_client.agents.upload_file_and_poll(file_path=file_path, purpose=FilePurpose.AGENTS)
        file_ids.append(file.id)
        print(f"Uploaded file, file ID: {file.id}")
        
        # Create vector store file
        project_client.agents.create_vector_store_file_and_poll(vector_store_id=vector_store.id, file_id=file.id)
        print(f"Added file to vector store: {file_path}")

    print(f"Total files processed: {len(file_ids)}")

    file_search_tool = FileSearchTool(vector_store_ids=[vector_store.id])

    botinstruction = None
    with open("./botinstruction.txt") as f:
        botinstruction = f.read()
    #project_client.telemetry.enable()
    agent = project_client.agents.update_agent(
            agent_id ="asst_OPLSmeJZc2lx9yDPMSiLScAV",
    #        assistant_id="asst_EEEwapkvCJdSlO4Lmz8b1jZo",
    #agent = project_client.agents.create_agent(
            model="gpt-4o", name="GCP-Agent-WebApp", 
            instructions=botinstruction, 
            tools=file_search_tool.definitions
    #     tool_resources=file_search_tool.resources,
    )
    
#bq_inputqueue = AzureFunctionStorageQueue( storage_service_endpoint= aztools.storage_connection_string, queue_name= aztools.input_queue_name)
#bq_outputqueue = AzureFunctionStorageQueue(storage_service_endpoint= aztools.storage_connection_string, queue_name= aztools.output_queue_name)
    
#bq_func = AzureFunctionTool(name="bq_run_job",  description="run a query against bigquery", 
#                            parameters=aztools.bq_function_params,
#                            input_queue = bq_inputqueue, output_queue = bq_outputqueue
#                            )

# Initialize agent toolset with user functions
#functions = FunctionTool(user_functions)
#toolset = ToolSet()
#toolset.add(functions)
#toolset.add(bq_func)
#toolset.add(file_search_tool)


def chat():
    
    agent = project_client.agents.get_agent(agent_id = "asst_OPLSmeJZc2lx9yDPMSiLScAV")
    print("Welcome to the conversation")
    # Create thread for communication
    thread = project_client.agents.create_thread()
    print(f"Created thread, ID: {thread.id}")
    while True:
        user_input = input("You: ")
     
        if len(user_input.strip()) == 0 :
            print("ChatBot: request can't be empty")
            continue

        if user_input.lower() in ["exit", "quit", "bye"]:
        
            print("ChatBot: Goodbye! Have a great day!")
            break
        
            # Create message to thread
        message = project_client.agents.create_message(
            thread_id=thread.id,
            role="user",
            content=user_input,
        )

        tset = ToolSet()
        tset.add(CodeInterpreterTool())

        run =  project_client.agents.create_and_process_run(thread_id= thread.id, agent_id = agent.id, toolset = tset)
            
        amessages = project_client.agents.list_run_steps(thread_id=thread.id, run_id=run.id)

        #print(amessages)
        amessages = project_client.agents.list_messages(thread_id=thread.id, run_id=run.id)

        #print(amessages)
        # The messages are following in the reverse order,
        # we will iterate them and output only text contents.
        for data_point in reversed(amessages.data):
            for message in data_point.content:
                if isinstance(message, MessageImageFileContent):
                    filecontent = project_client.agents.get_file_content(message.image_file.file_id)
                    chunks = []

                    for chunk in filecontent:
                        chunks.append(chunk)
                    
                    
                    print(f"{data_point.role}: {chunks}")
                
if __name__ == "__main__":
    ConfigureAgent()
    #chat()
    print("test")
   
