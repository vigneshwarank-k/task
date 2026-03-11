from llm.llm_config import chat_llm
from rag.rag_pipeline import retriever
from state.agentstate import GroceryState
from langchain_core.messages import HumanMessage, SystemMessage


def rag_retriever_node(state: GroceryState):

    try:
        mcp = state.get("mcp_command", {})

        question = mcp.get("parameters", {}).get("question")

        if not question:
            question = state.get("user_query")

        docs = retriever.invoke(question)

        context = "\n\n".join([doc.page_content for doc in docs])

        system_prompt = SystemMessage(
            content=f"""
You are a grocery store product expert.

Use the provided context to answer the user question.

CONTEXT:
{context}

Rules:
- Answer only using the context
- If answer not found, say "I don't know".
"""
        )

        response = chat_llm.invoke([system_prompt, HumanMessage(content=question)])

        return {"knowledge_result": response.content}

    except Exception as e:
        return {"knowledge_erros": str(e)}
