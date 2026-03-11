from typing import TypedDict, Optional


class GroceryState(TypedDict):
    user_query: str
    mcp_command: Optional[dict]
    inventory_result: Optional[dict]
    knowledge_result: Optional[str]
    final_answer: Optional[str]
    extract_product_errors: Optional[str]
    knowledge_errors: Optional[str]
