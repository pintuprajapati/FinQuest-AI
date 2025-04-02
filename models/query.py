from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

class Query(BaseModel):
    id: Optional[str] = None
    query_text: str
    embedding_vector: Optional[List[float]] = None
    response: Optional[str] = None
    created_at: datetime = datetime.now()
    
class SearchResult(BaseModel):
    document_id: str
    chunk_id: str
    content: str
    similarity: float
    metadata: Dict[str, Any] = {} 