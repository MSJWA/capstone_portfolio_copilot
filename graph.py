from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator
from agents.router import real_router, extract_holding_details
from agents.action_agents import add_holding, get_portfolio_value
from agents.rag_agents import answer_company_question

class GraphState(TypedDict):
    user_id: str
    message: str
    route: str
    reply: str
    tools_called: Annotated[list, operator.add]

def router_node(state: GraphState) -> GraphState:
    route = real_router(state["message"])
    return {"route": route, "tools_called": []}

def action_node(state: GraphState) -> GraphState:
    message = state["message"]
    if "bought" in message.lower() or "buy" in message.lower():
        details = extract_holding_details(message)
        if details:
            reply = add_holding(state["user_id"], details["ticker"], details["quantity"], details["avg_cost"])
            return {"reply": reply, "tools_called": ["extract_holding_details", "add_holding"]}
        return {"reply": "I couldn't understand the purchase details.", "tools_called": ["extract_holding_details"]}
    reply = get_portfolio_value(state["user_id"])
    return {"reply": reply, "tools_called": ["get_portfolio_value"]}

def rag_node(state: GraphState) -> GraphState:
    reply = answer_company_question(state["message"])
    return {"reply": reply, "tools_called": ["answer_company_question"]}

def general_node(state: GraphState) -> GraphState:
    return {"reply": "General chat response.", "tools_called": []}

def route_decision(state: GraphState) -> str:
    return state["route"]

graph = StateGraph(GraphState)
graph.add_node("router", router_node)
graph.add_node("action", action_node)
graph.add_node("rag", rag_node)
graph.add_node("general", general_node)

graph.set_entry_point("router")
graph.add_conditional_edges("router", route_decision, {
    "action": "action",
    "rag": "rag",
    "general": "general"
})
graph.add_edge("action", END)
graph.add_edge("rag", END)
graph.add_edge("general", END)

app_graph = graph.compile()

if __name__ == "__main__":
    result = app_graph.invoke({"user_id": "test_user", "message": "why did SAZEW go up?", "route": "", "reply": "", "tools_called": []})
    print(result)