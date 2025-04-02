from typing import List, Union, Dict, Any
from sentence_transformers import SentenceTransformer
import uuid

from models.document import DocumentChunk
from models.embeddings import Embedding
from models.query import Query
from core.config import settings

class EmbeddingGenerator:
    """
    Generates embeddings for document chunks and queries
    """
    
    def __init__(self, model_name: str = None):
        self.model_name = model_name or settings.EMBEDDING_MODEL
        self.model = SentenceTransformer(self.model_name)
    
    def embed_chunks(self, chunks: List[DocumentChunk]) -> List[Embedding]:
        """Convert document chunks to embeddings"""
        texts = [chunk.content for chunk in chunks]
        embedding_vectors = self.model.encode(texts)
        
        embeddings = []
        for i, chunk in enumerate(chunks):
            embedding = Embedding(
                id=str(uuid.uuid4()),
                chunk_id=chunk.id,
                document_id=chunk.document_id,
                embedding_vector=embedding_vectors[i].tolist(),
                model_name=self.model_name,
                metadata=chunk.metadata
            )
            embeddings.append(embedding)
        
        return embeddings
    
    def embed_query(self, query: Union[str, Query]) -> List[float]:
        """Convert a query to embedding vector"""
        if isinstance(query, str):
            query_text = query
        else:
            query_text = query.query_text
            
        embedding_vector = self.model.encode(query_text)
        return embedding_vector.tolist() 