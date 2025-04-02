from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

class Embedding(BaseModel):
    id: Optional[str] = None
    chunk_id: str
    document_id: str
    embedding_vector: List[float]
    model_name: str
    metadata: Dict[str, Any] = {}
    created_at: datetime = datetime.now() 