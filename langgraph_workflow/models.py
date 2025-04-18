from pydantic import BaseModel
from typing import TypedDict, Any

from langchain.schema import Document
from langchain_core.messages import BaseMessage

class ChatRequest(BaseModel):
    question: str
    
# Define state schema
class WorkflowState(TypedDict):
    question: str               # Current user message
    messages: list[BaseMessage] # Full message history (for chat context)
    prompt: str                 # Formatted prompt sent to LLM
    context: list[Document]     # Retrieved context chunks from vector DB
    answer: str                 # Final response to user
    on_topic: str               # Topic category (e.g., loan, tax, etc.)
    
    intent: str                 # Intent label: "greetings", "math", "faq", "chit-chat", etc.
    last_intent: str            # Most recent valid domain intent
    clarification_required: bool# Most recent valid domain intent
    flags: dict[str, Any]       # Flexible storage for other behaviors (e.g., manipulation_detected, needs_followup)
    