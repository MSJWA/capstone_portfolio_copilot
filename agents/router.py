import os
from groq import Groq
from dotenv import load_dotenv
import json

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def real_router(message: str) -> str:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a router. Classify the user's message into exactly "
                    "one category: 'action' (buying/selling/updating holdings, or "
                    "asking for portfolio value/breakdown), 'rag' (asking why "
                    "something happened, or asking about a company), or 'general' "
                    "(anything else, like greetings). Respond with ONLY the single "
                    "word: action, rag, or general. No punctuation, no explanation."
                )
            },
            {"role": "user", "content": message}
        ],
        max_tokens=5
    )
    route = response.choices[0].message.content.strip().lower()

    if route not in ["action", "rag", "general"]:
        route = "general"

    return route

def extract_holding_details(message: str) -> dict | None:
    tools = [
        {
            "type": "function",
            "function": {
                "name": "add_holding",
                "description": "Extract stock purchase details from a message",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "ticker": {"type": "string", "description": "Stock ticker symbol, e.g. LUCK"},
                        "quantity": {"type": "number"},
                        "avg_cost": {"type": "number", "description": "Price per share"}
                    },
                    "required": ["ticker", "quantity", "avg_cost"]
                }
            }
        }
    ]

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": message}],
        tools=tools
    )

    message_obj = response.choices[0].message
    if message_obj.tool_calls:
        args = json.loads(message_obj.tool_calls[0].function.arguments)
        return args
    return None