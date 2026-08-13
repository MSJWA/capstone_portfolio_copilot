from fastapi import FastAPI
from models import UserRequest, AgentResponse
from agents.router import real_router
from agents.action_agents import add_holding, get_portfolio_value
from agents.router import real_router, extract_holding_details
from agents.rag_agents import answer_company_question
import uuid


app = FastAPI()

@app.post("/chat", response_model=AgentResponse)
def chat(request: UserRequest):
    request_id = str(uuid.uuid4())
    route = real_router(request.message)

    if route == "action":
        if "bought" in request.message.lower() or "buy" in request.message.lower():
            details = extract_holding_details(request.message)
            if details:
                reply = add_holding(request.user_id, details["ticker"], details["quantity"], details["avg_cost"])
                tools_called = ["extract_holding_details", "add_holding"]

            else:
                    reply = "I couldn't understand the purchase details — could you rephrase?"
                    tools_called = ["extract_holding_details"]
        else:
            reply = get_portfolio_value(request.user_id)
            tools_called = ["get_portfolio_value"]
    elif route == "rag":
        reply = answer_company_question(request.message)
        tools_called = ["answer_company_question"]
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