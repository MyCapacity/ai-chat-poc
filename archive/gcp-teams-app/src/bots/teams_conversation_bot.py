# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os
import json
import time
from typing import List

from botbuilder.core import (
    ActivityHandler,
    TurnContext,
    UserState,
    CardFactory,
    MessageFactory,
    BotTelemetryClient,
    NullTelemetryClient,
)
from botbuilder.schema import (
    ChannelAccount,
    HeroCard,
    CardImage,
    CardAction,
    ActionTypes,
)

from botbuilder.schema.teams import (
    TeamsChannelAccount,
    TeamsChannelData
)

from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    AgentEventHandler,
    AgentStreamEvent,
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
    MessageImageFileContent,
    ToolOutput,
    CodeInterpreterTool,
)
import time
import asyncio
import threading
from datetime import datetime
# Your custom Python functions (for "fetch_weather","fetch_stock_price","send_email","fetch_datetime", etc.)
from bots.enterprise_functions import enterprise_fns
from data_models import MessageThreadContext
import base64


# Define a Custom Event Handler
class StreamEventHandler(AgentEventHandler):
    def __init__(self, client, functions: FunctionTool):
        super().__init__()
        self._current_message_id = None
        self._accumulated_text = ""
        self.functions = functions
        self.client = client

    def on_message_delta(self, delta: MessageDeltaChunk) -> None:
        None

    def on_thread_message(self, message: ThreadMessage) -> None:
        None

    def on_thread_run(self, run: ThreadRun) -> None:
        #print(f"status > {run.status.name.lower()}")
        if run.status == "failed":
            print(f"error > {run.last_error}")

        if run.status == "requires_action" and isinstance(run.required_action, SubmitToolOutputsAction):
            tool_calls = run.required_action.submit_tool_outputs.tool_calls

            tool_outputs = []
            for tool_call in tool_calls:
                if isinstance(tool_call, RequiredFunctionToolCall):
                    try:
                        output = self.functions.execute(tool_call)
                        tool_outputs.append(
                            ToolOutput(
                                tool_call_id=tool_call.id,
                                output=output,
                            )
                        )
                    except Exception as e:
                        print(f"Error executing tool_call {tool_call.id}: {e}")
                        raise e

            #print(f"Tool outputs: {tool_outputs}")
            if tool_outputs:
                # Once we receive 'requires_action' status, the next event will be DONE.
                # Here we associate our existing event handler to the next stream.
                self.client.agents.submit_tool_outputs_to_stream(
                    thread_id=run.thread_id, run_id=run.id, tool_outputs=tool_outputs, event_handler=self
                )

    def on_run_step(self, step: RunStep) -> None:
        print(f"{step.type.name.lower()} > {step.status.name.lower()}")

    """
     def on_run_step_delta(self, delta: RunStepDeltaChunk) -> None:
        # If partial tool calls come in, we log them
        if delta.delta.step_details and delta.delta.step_details.tool_calls:
            for tcall in delta.delta.step_details.tool_calls:
                if getattr(tcall, "function", None):
                    if tcall.function.name is not None:
                        print(f"tool call > {tcall.function.name}")
    """

    def on_unhandled_event(self, event_type: str, event_data):
        None
        #print(f"unhandled > {event_type} > {event_data}")

    def on_error(self, data: str) -> None:
        print(f"error > {data}")

    def on_done(self) -> None:
        print("done")

        

class TeamsConversationBot(ActivityHandler):
    def __init__(self, openaikey: str, agentid: str, user_state:UserState, telemetry_client: BotTelemetryClient):
        self._ai_connection = openaikey
        self._agent_id = agentid
        self.client = None
        self._user_state = user_state
        self.user_state_accessor = self._user_state.create_property("MessageThreadContext")
        self.telemetry_client = telemetry_client
        self.last_client_check = 0
        self.client_check_interval = 300  # Check client every 5 minutes
        self.reconnect_client()

        found_agent = self.client.agents.get_agent(self._agent_id)

        if not found_agent:
            raise ValueError(f"Agent with name '{AGENT_NAME}' not found.")

        agent_id = found_agent.id
        print(f"Using agent > {found_agent.name} (id: {agent_id})")

                
        VECTOR_STORE_NAME = "BqVectorStore"
        #all_vector_stores = self.client.agents.list_vector_stores().data
        #existing_vector_store = next(
        #    (store for store in all_vector_stores if store.name == VECTOR_STORE_NAME),
        #    None
        #)

        vector_store_id = "vs_KUMlc94nUtHx88QpNJ8xC4Lx"
        #if existing_vector_store:
        #    vector_store_id = existing_vector_store.id
        #    print(f"reusing vector store > {existing_vector_store.name} (id: {existing_vector_store.id})")

        file_search_tool = None
        if vector_store_id:
            file_search_tool = FileSearchTool(vector_store_ids=[vector_store_id])
            print(f"file search > connected {vector_store_id}")


        self.toolset = ToolSet()
        if file_search_tool:
            self.toolset.add(file_search_tool)

        self.custom_functions = FunctionTool(enterprise_fns)

        codeinterpreter = CodeInterpreterTool()
        self.toolset.add(self.custom_functions)
        self.toolset.add(codeinterpreter)

        self.agent = self.client.agents.update_agent(
            agent_id=found_agent.id,
            model=found_agent.model,
            instructions=found_agent.instructions,
            toolset=self.toolset,
        )

        print(f"reusing agent > {self.agent.name} (id: {self.agent.id})")

     

    def reconnect_client (self):
        
        try:
           credential = DefaultAzureCredential()
           self.client = AIProjectClient.from_connection_string(
               credential=credential,
               conn_str=self._ai_connection
           )
           print("Client reconnected successfully")
           self.last_client_check = time.time()
           return True
           
        except Exception as e:
           print(f"Failed to reconnect client: {str(e)}")
           return False

    def ensure_client_active(self) -> bool:
        """Ensure the client is active, reconnect if necessary."""
        current_time = time.time()
        # Check if we need to verify client status
        if current_time - self.last_client_check >= self.client_check_interval:
            if not self.reconnect_client():
                return False
            self.last_client_check = current_time
        
        return True

    async def on_turn(self, turn_context: TurnContext):
        await super().on_turn(turn_context)
        # save changes to WelcomeUserState after each turn
        await self._user_state.save_changes(turn_context)


    async def on_members_added_activity(  # pylint: disable=unused-argument
        self,
        teams_members_added: [TeamsChannelAccount],
        turn_context: TurnContext,
    ):
        for member in teams_members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity(
                    f"Welcome to the team { member }. "
                )

    async def on_message_activity(self, turn_context: TurnContext):


        # Ensure client is active before processing
      
        if not self.ensure_client_active():
            await turn_context.send_activity("I'm having trouble connecting to my services. Please try again in a moment.")
            return
        # Get the state properties from the turn context.
        threadContext = await self.user_state_accessor.get(
            turn_context, MessageThreadContext
        )

        # Let the AI process the message (this will invoke functions as needed)
        text = turn_context.activity.text.strip().lower()
        if text.strip().lower() in ["restart","reset","end", "stop", "exit"] :
            threadContext.threadid = None
            await turn_context.send_activity("Restarting the conversation.")        
            return 

        localclient = self.client

        thread = None
        try:
            if not threadContext.threadid:
                raise Exception("thread not started")
            thread = localclient.agents.get_thread(threadContext.threadid)
        
        except Exception as error:
            print(f"caught error for expired thread: {error}")
            thread = localclient.agents.create_thread()
            threadContext.threadid = thread.id
            print(f"started new thread {thread.id}")

        message = localclient.agents.create_message(thread_id=thread.id, role="user", content=text)    

        start = datetime.now().timestamp()

        with localclient.agents.create_stream(
            thread_id=thread.id, 
            agent_id=self._agent_id, 
            tools = self.toolset.definitions,
            event_handler=StreamEventHandler(client=localclient, functions=self.custom_functions)
        ) as stream:
            for event_type, event_data, _ in stream:
                if isinstance(event_data, MessageDeltaChunk):
                    None
                    #continue
                elif isinstance(event_data, ThreadMessage):
                    if event_data.role == "assistant": #and event_data.created_at.timestamp() > start:
                        for last_message_content in event_data.content:
                            if isinstance(last_message_content, MessageTextContent):
                                await turn_context.send_activity(last_message_content.text.value) 
                            elif isinstance(last_message_content, MessageImageFileContent):
                                try : 
                                    filecontent = localclient.agents.get_file_content(last_message_content.image_file.file_id)
                                    chunks = []

                                    for chunk in filecontent:
                                        chunks.append(chunk)
                                    
                                    combined_bytes = b''.join(chunks)
                                    base64_image = base64.b64encode(combined_bytes).decode('utf-8')
                                    
                                    # Create data URI for the image
                                    image_uri = f"data:image/png;base64,{base64_image}"
                                    
                                    card = HeroCard(
                                        images=[CardImage(url=image_uri)]
                                    )
                                    m = MessageFactory.attachment(CardFactory.hero_card(card))
                                    await turn_context.send_activity(m)

                                except Exception as error : 
                                    await turn_context.send_activity(f"failed to retrieve image file {last_message_content.image_file.file_id} {error}")
                elif isinstance(event_data, ThreadRun):
                    None
                    #await turn_context.send_activity(f"ThreadRun status: {event_data.status}")
                elif isinstance(event_data, RunStep):
                    None
                    #await turn_context.send_activity(f"RunStep type: {event_data.type}, Status: {event_data.status}")
                elif event_type == AgentStreamEvent.ERROR:
                    await turn_context.send_activity(f"An error occurred. Data: {event_data}")
                elif event_type == AgentStreamEvent.DONE:
                    print(f"{event_type}" )
                    #await turn_context.send_activity("Stream completed.")
                    #break
                else:
                    None
                    #print(f"Unhandled Event Type: {event_type}, Data: {event_data}")

        print(f"exit stream {thread.id}")
        """
        run = localclient.agents.create_and_process_run(thread_id=thread.id, agent_id=self._agent_id, toolset = self.toolset)

        outputs = localclient.agents.list_messages(thread_id=thread.id, run_id=run.id)

        # The messages are following in the reverse order,
        # we will iterate them and output only text contents.
        for data_point in reversed(outputs.data):
            if data_point.role == "assistant" and data_point.created_at.timestamp() > start:
                for last_message_content in data_point.content:
                    if isinstance(last_message_content, MessageTextContent):
                        await turn_context.send_activity(last_message_content.text.value) 
                    elif isinstance(last_message_content, MessageImageFileContent):
                        try : 
                            filecontent = localclient.agents.get_file_content(last_message_content.image_file.file_id)
                            chunks = []

                            for chunk in filecontent:
                                chunks.append(chunk)
                            
                            combined_bytes = b''.join(chunks)
                            base64_image = base64.b64encode(combined_bytes).decode('utf-8')
                            
                            # Create data URI for the image
                            image_uri = f"data:image/png;base64,{base64_image}"
                            
                            card = HeroCard(
                                images=[CardImage(url=image_uri)]
                            )
                            m = MessageFactory.attachment(CardFactory.hero_card(card))
                            await turn_context.send_activity(m)

                        except Exception as error : 
                            await turn_context.send_activity(f"failed to retrieve image file {last_message_content.image_file.file_id} {error}")  
        return
        """

    #async def on_turn(self, turn_context: TurnContext): 
        
    

    async def _get_paged_members(
        self, turn_context: TurnContext
    ) -> List[ChannelAccount]:
        paged_members = []
        continuation_token = None

        while True:
            current_page = await TeamsInfo.get_paged_members(
                turn_context, continuation_token, 100
            )
            continuation_token = current_page.continuation_token
            paged_members.extend(current_page.members)

            if continuation_token is None:
                break

        return paged_members

    async def _delete_card_activity(self, turn_context: TurnContext):
        await turn_context.delete_activity(turn_context.activity.reply_to_id)

    @property
    def telemetry_client(self) -> BotTelemetryClient:
        """
        Gets the telemetry client for logging events.
        """
        return self._telemetry_client

    # pylint:disable=attribute-defined-outside-init
    @telemetry_client.setter
    def telemetry_client(self, value: BotTelemetryClient) -> None:
        """
        Sets the telemetry client for logging events.
        """
        if value is None:
            self._telemetry_client = NullTelemetryClient()
        else:
            self._telemetry_client = value