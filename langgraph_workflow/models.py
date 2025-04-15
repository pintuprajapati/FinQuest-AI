from pydantic import BaseModel
from typing import TypedDict

from langchain.schema import Document
from langchain_core.messages import BaseMessage

class ChatRequest(BaseModel):
    question: str
    
# Define state schema
class WorkflowState(TypedDict):
    question: str
    messages: list[BaseMessage]
    prompt: str
    context: list[Document]
    answer: str
    on_topic: str
    