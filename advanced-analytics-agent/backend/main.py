"""
Production server
"""

from dotenv import load_dotenv
if __name__ == "__main__":
    load_dotenv()

import os
from fastapi.responses import JSONResponse
import uvicorn
from fastapi import FastAPI, Request
from ag_ui_adk import ADKAgent, add_adk_fastapi_endpoint
from agents.DataAnalyticsAgent.agent import root_agent

USER_ID_HEADER = "X-Goog-Authenticated-User-Id"

app = FastAPI()
adk_agent = ADKAgent(
    adk_agent=root_agent,
    session_timeout_seconds=3600,
    use_in_memory_services=True,
    user_id_extractor=lambda input: input.state.get("headers", {}).get("goog_authenticated_user_id", "local")
)
add_adk_fastapi_endpoint(app, adk_agent, path="/", extract_headers=[USER_ID_HEADER])

@app.get("/")
def index():
    return "Server running"

@app.get("/api/sessions")
def list_session(request: Request):
    user = "local"
    if USER_ID_HEADER in request.headers: 
        user = request.headers.get("X-Goog-Authenticated-User-Id")
    return JSONResponse({"sessions": list(adk_agent._session_manager._user_sessions.get(user, []))})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8081)))