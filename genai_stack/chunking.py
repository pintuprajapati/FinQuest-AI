import uuid
from typing import List, Dict, Any

from models.document import Document, DocumentChunk
from core.config import settings

class TextChunker:
    """
    Handles text chunking for document processing
    """
    
    def __init__(self, chunk_size: int = None, chunk_overlap: int = None):
        self.chunk_size = chunk_size or settings.CHUNK_SIZE
        self.chunk_overlap = chunk_overlap or settings.CHUNK_OVERLAP
    
    def chunk_text(self, document: Document, text: str) -> List[DocumentChunk]:
        """
        Split document text into chunks with overlap
        """
        chunks = []
        
        # Simple text chunking by characters with overlap
        for i in range(0, len(text), self.chunk_size - self.chunk_overlap):
            chunk_text = text[i:i + self.chunk_size]
            if not chunk_text.strip():
                continue
                
            chunk = DocumentChunk(
                id=str(uuid.uuid4()),
                document_id=document.id,
                content=chunk_text,
                chunk_index=len(chunks),
                metadata={
                    "start_char": i,
                    "end_char": min(i + self.chunk_size, len(text)),
                    "document_name": document.filename
                }
            )
            chunks.append(chunk)
        
        return chunks 