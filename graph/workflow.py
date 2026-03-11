from langgraph.graph import StateGraph, END
from state.agentstate import GroceryState

from agents.router_agent import query_router_node
from agents.inventory_agent import db_inventory_node
from agents.knowledge_agent import rag_retriever_node
from agents.recommendation_agent import recommendation_agent_node


builder = StateGraph(GroceryState)

# Add agent nodes
builder.add_node("router", query_router_node)
builder.add_node("inventory_agent", db_inventory_node)
builder.add_node("knowledge_agent", rag_retriever_node)
builder.add_node("recommendation_agent", recommendation_agent_node)


# Router decision function
def route_command(state: GroceryState):
    command = state["mcp_command"]["command"]

    if command == "inventory_lookup":
        return "inventory_only"

    elif command == "knowledge_query":
        return "knowledge_only" 

    elif command == "recommend_products":
        return "knowledge_agent"  

    elif command == "combined_query":
        return "combined"  

    return END


# Entry point
builder.set_entry_point("router")


# Router conditional edges
builder.add_conditional_edges(
    "router",
    route_command,
    {
        "inventory_only": "inventory_agent",
        "knowledge_only": "knowledge_agent",
        "knowledge_agent": "knowledge_agent",
        "combined": "knowledge_agent", 
    },
)

builder.add_edge("knowledge_agent", "inventory_agent")
builder.add_edge("inventory_agent", "recommendation_agent")
builder.add_edge("recommendation_agent", END)

graph = builder.compile()


try:
    image = graph.get_graph().draw_mermaid_png()

    with open("graph.png", "wb") as file:
        file.write(image)

    print("Image created successfully")

except Exception as e:
    print("Error creating image:", str(e))
