# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import sys
import traceback
import uuid
from datetime import datetime
from http import HTTPStatus

from aiohttp import web
from aiohttp.web import Request, Response, json_response
from botbuilder.core import (
    MemoryStorage,
    TurnContext,
    UserState,
)
from botbuilder.core.integration import aiohttp_error_middleware
from botbuilder.integration.aiohttp import CloudAdapter, ConfigurationBotFrameworkAuthentication
from botbuilder.schema import Activity, ActivityTypes
from botbuilder.applicationinsights import ApplicationInsightsTelemetryClient
from botbuilder.integration.applicationinsights.aiohttp import (
    AiohttpTelemetryProcessor,
    bot_telemetry_middleware,
)

from bots import TeamsConversationBot
from config import Config
from data_models import MessageThreadContext 


CONFIG = Config()

if not CONFIG.APP_ID :
    CONFIG.APP_ID = f"{uuid.uuid1()}"
    CONFIG.APP_TENANTID = f"{uuid.uuid1()}"
    CONFIG.APP_TYPE = f"MultiTenant"
# Create adapter.
ADAPTER = CloudAdapter(ConfigurationBotFrameworkAuthentication(CONFIG))



# Catch-all for errors.
async def on_error(context: TurnContext, error: Exception):
    debug = True
    # This check writes out errors to console log .vs. app insights.
    # NOTE: In production environment, you should consider logging this to Azure
    #       application insights.
    print(f"\n [on_turn_error] unhandled error: {error}", file=sys.stderr)
    traceback.print_exc()

    # Send a message to the user
    await context.send_activity("The bot encountered an error or bug.")
    await context.send_activity(
        f"To continue to run this bot, please fix the bot source code."
    )
    # Send a trace activity if we're talking to the Bot Framework Emulator
    if debug:
        await context.send_activity(f"{error}")

ADAPTER.on_turn_error = on_error


# Create MemoryStorage, UserState
MEMORY = MemoryStorage()
USER_STATE = UserState(MEMORY)

# Create telemetry client.
# Note the small 'client_queue_size'.  This is for demonstration purposes.  Larger queue sizes
# result in fewer calls to ApplicationInsights, improving bot performance at the expense of
# less frequent updates.
INSTRUMENTATION_KEY = CONFIG.APPINSIGHTS_INSTRUMENTATIONKEY
TELEMETRY_CLIENT = ApplicationInsightsTelemetryClient(
    INSTRUMENTATION_KEY, telemetry_processor=AiohttpTelemetryProcessor(), client_queue_size=10
)
# Create the Bot
BOT = TeamsConversationBot(CONFIG.AZURE_OPENAI_API_KEY, CONFIG.AZURE_OPENAI_ASSISTANT_ID, USER_STATE, TELEMETRY_CLIENT)


# Listen for incoming requests on /api/messages.
async def messages(req: Request) -> Response:
    return await ADAPTER.process(req, BOT)

# Hello World route handler
async def hello_world(req: Request) -> Response:
    return web.Response(
        text="Hello, World! Welcome to the Teams Bot API",
        content_type='text/plain'
    )

def init_func(argv):
    APP = web.Application(middlewares=[aiohttp_error_middleware])
    APP.router.add_post("/api/messages", messages)
    APP.router.add_get("/", hello_world)  # Add root route for hello world
    return APP

if __name__ == "__main__":
    APP = init_func(None)
    try:
        web.run_app(APP, host="localhost", port=CONFIG.PORT)
    except Exception as error:
        raise error
