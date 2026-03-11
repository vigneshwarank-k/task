from llm.llm_config import chat_llm
from langchain_core.messages import SystemMessage, HumanMessage
from state.agentstate import GroceryState
import json


def query_router_node(state: GroceryState) -> GroceryState:

    user_question = state["user_query"]

    system_prompt = SystemMessage(
    content="""
You are a Query Router for a Grocery AI system.

Available commands:

1. inventory_lookup — user asks about stock, price, availability only
2. knowledge_query — user asks about product knowledge only  
3. recommend_products — user asks for suggestions only
4. combined_query — user asks BOTH knowledge AND inventory in one question

Example for combined_query:
User: Is basmati rice good for biryani and do you have it in stock?
Output:
{
  "command": "combined_query",
  "parameters": {
    "question": "Is basmati rice good for biryani?",
    "product": "basmati rice"
  }
}

IMPORTANT: Return ONLY valid JSON.
"""
)

    response = chat_llm.invoke([system_prompt, HumanMessage(content=user_question)])

    try:
        mcp_command = json.loads(response.content)
    except:
        mcp_command = {
            "command": "knowledge_query",
            "parameters": {"question": user_question},
        }

    return {"mcp_command": mcp_command}
