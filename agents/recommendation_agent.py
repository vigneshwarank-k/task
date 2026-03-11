from llm.llm_config import chat_llm
from state.agentstate import GroceryState
from langchain_core.messages import SystemMessage, HumanMessage


def recommendation_agent_node(state: GroceryState) -> GroceryState:

    try:
        knowledge = state.get("knowledge_result", "")
        inventory = state.get("inventory_result", {})

        system_prompt = SystemMessage(
            content="""
You are a grocery recommendation assistant.

Your job is to combine product knowledge and inventory data
and provide a final helpful recommendation to the user.

Rules:
- If product is available, recommend it
- Mention price and aisle
- If not available, suggest alternatives
"""
        )

        human_prompt = HumanMessage(
            content=f"""
User Question:
{state.get("user_query")}

Knowledge Result:
{knowledge}

Inventory Result:
{inventory}

Generate the final answer for the user.
"""
        )

        response = chat_llm.invoke([system_prompt, human_prompt])

        return {"final_answer": response.content}

    except Exception as e:
        return {"final_answer": f"Error generating recommendation: {str(e)}"}
