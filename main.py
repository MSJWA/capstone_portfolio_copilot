from fastapi import FastAPI
from pydantic import BaseModel
from typing import Literal
import uuid

app = FastAPI()

class UserRequest(BaseModel):
    user_id: str
    message: str

class AgentResponse(BaseModel):
    reply: str
    agent_used: Literal["router", "action", "rag"]
    tool_calls_made: list[str]
    tokens_used: int
    estimated_cost_usd: float
    request_id: str

def mock_router(message: str) -> str:
    if "bought" in message.lower() or "portfolio" in message.lower():
        return "action"
    elif "why" in message.lower() or "what" in message.lower():
        return "rag"
    else:
        return "router"

def mock_action_tool(message: str) -> str:
    return "Mock: added holding to portfolio (fake data)."

def mock_rag_tool(message: str) -> str:
    return "Mock: this is a fake answer pulled from fake company notes."

@app.post("/chat", response_model=AgentResponse)
def chat(request: UserRequest):
    request_id = str(uuid.uuid4())
    route = mock_router(request.message)

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