from pydantic import BaseModel
from typing import Dict, Any


class MCPMessage(BaseModel):
    command: str
    parameters: Dict[str, Any]
    source_agent: str
    target_agent: str
