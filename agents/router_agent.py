from llm.llm_config import chat_llm
from langchain_core.messages import SystemMessage, HumanMessage
from state.agentstate import GroceryState
from schemas.mcp_schema import MCPMessage


def query_router_node(state: GroceryState) -> GroceryState:

    user_question = state["user_query"]

    system_prompt = SystemMessage(
        content="""
You are the Query Router Agent for a Grocery AI system.
You are the first agent that receives the request.

Responsibilities:
- Understand the query
- Convert it into an MCP (Message Command Protocol) command
- Send request to other agents using A2A

Available commands:
1. inventory_lookup — user asks about stock, price, availability only
2. knowledge_query — user asks about product knowledge only  
3. recommend_products — user asks for suggestions only
4. combined_query — user asks BOTH knowledge AND inventory in one question

Example MCP message for inventory_lookup:
User: Do you have basmati rice?
Output:
{
  "command": "inventory_lookup",
  "parameters": {"product": "basmati rice"},
  "source_agent": "router_agent",
  "target_agent": "inventory_agent"
}

Example MCP message for knowledge_query:
User: Which rice is best for biryani?
Output:
{
  "command": "knowledge_query",
  "parameters": {"question": "Which rice is best for biryani?"},
  "source_agent": "router_agent",
  "target_agent": "knowledge_agent"
}

Example MCP message for combined_query:
User: Is basmati rice good for biryani and do you have it in stock?
Output:
{
  "command": "combined_query",
  "parameters": {
    "question": "Is basmati rice good for biryani?",
    "product": "basmati rice"
  }
  "source_agent": "router_agent",
  "target_agent": "inventory_agent"
}
"""
    )
    
    structured_llm = chat_llm.with_structured_output(MCPMessage)
    
    try:
        response = structured_llm.invoke([system_prompt, HumanMessage(content=user_question)])
        mcp_command = response.model_dump()
    except Exception as e:
        mcp_command = {
            "command": "knowledge_query",
            "parameters": {"question": user_question},
            "source_agent": "router_agent",
            "target_agent": "knowledge_agent"
        }

    return {"mcp_command": mcp_command}
