from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class DocumentProcessRequest(BaseModel):
    file_url: str

class DocumentStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    PROCESSED = "processed"
    FAILED = "failed"

class DocumentType(str, Enum):
    PDF = "pdf"
    DOCX = "docx"
    TXT = "txt"
    OTHER = "other"
    IMAGE = "image"
    AUDIO = "audio"

class Document(BaseModel):
    id: Optional[str] = None
    filename: str
    file_path: str
    document_type: DocumentType
    status: DocumentStatus = DocumentStatus.PENDING
    metadata: Dict[str, Any] = {}
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

class DocumentChunk(BaseModel):
    id: Optional[str] = None
    document_id: str
    content: str
    metadata: Dict[str, Any] = {}
    chunk_index: int 