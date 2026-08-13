from pydantic import BaseModel
from typing import Literal

class UserRequest(BaseModel):
    user_id: str
    message: str

class AgentResponse(BaseModel):
    reply: str
    agent_used: Literal["router", "action", "rag", "general"]
    tool_calls_made: list[str]
    tokens_used: int
    estimated_cost_usd: float
    request_id: str