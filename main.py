from fastapi import FastAPI
from models import UserRequest, AgentResponse
from agents.router import real_router
import uuid

app = FastAPI()

def mock_action_tool(message: str) -> str:
    return "Mock: added holding to portfolio (fake data)."

def mock_rag_tool(message: str) -> str:
    return "Mock: this is a fake answer pulled from fake company notes."

@app.post("/chat", response_model=AgentResponse)
def chat(request: UserRequest):
    request_id = str(uuid.uuid4())
    route = real_router(request.message)

    if route == "action":
        reply = mock_action_tool(request.message)
        tools_called = ["mock_action_tool"]
    elif route == "rag":
        reply = mock_rag_tool(request.message)
        tools_called = ["mock_rag_tool"]
    else:
        reply = "Mock: general chat response."
        tools_called = []

    return AgentResponse(
        reply=reply,
        agent_used=route,
        tool_calls_made=tools_called,
        tokens_used=0,
        estimated_cost_usd=0.0,
        request_id=request_id
    )