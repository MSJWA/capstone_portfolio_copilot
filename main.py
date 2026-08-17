from fastapi import FastAPI
from models import UserRequest, AgentResponse
from graph import app_graph
import uuid

app = FastAPI()

@app.post("/chat", response_model=AgentResponse)
def chat(request: UserRequest):
    request_id = str(uuid.uuid4())

    result = app_graph.invoke({
        "user_id": request.user_id,
        "message": request.message,
        "route": "",
        "reply": "",
        "tools_called": []
    })

    return AgentResponse(
        reply=result["reply"],
        agent_used=result["route"],
        tool_calls_made=result["tools_called"],
        tokens_used=0,
        estimated_cost_usd=0.0,
        request_id=request_id
    )