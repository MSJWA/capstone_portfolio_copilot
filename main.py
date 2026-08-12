from fastapi import FastAPI
from models import UserRequest, AgentResponse
from agents.router import real_router
from agents.action_agents import add_holding, get_portfolio_value
import uuid

app = FastAPI()

def mock_rag_tool(message: str) -> str:
    return "Mock: this is a fake answer pulled from fake company notes."

@app.post("/chat", response_model=AgentResponse)
def chat(request: UserRequest):
    request_id = str(uuid.uuid4())
    route = real_router(request.message)

    if route == "action":
        if "portfolio" in request.message.lower() or "worth" in request.message.lower():
            reply = get_portfolio_value(request.user_id)
            tools_called = ["get_portfolio_value"]
        else:
            reply = "Action agent recognized this, but adding holdings via chat isn't wired up yet — use the direct function for now."
            tools_called = ["add_holding (not yet connected)"]
    elif route == "rag":
        reply = mock_rag_tool(request.message)
        tools_called = ["mock_rag_tool"]
    else:
        reply = "General chat response."
        tools_called = []

    return AgentResponse(
        reply=reply,
        agent_used=route,
        tool_calls_made=tools_called,
        tokens_used=0,
        estimated_cost_usd=0.0,
        request_id=request_id
    )