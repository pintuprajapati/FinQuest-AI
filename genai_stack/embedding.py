from typing import List, Union, Dict, Any
from langchain_openai.embeddings import OpenAIEmbeddings
import uuid

from models.document import DocumentChunk
from models.embeddings import Embedding
from models.query import Query
from core.config import settings
import custom_log as log
import time

class EmbeddingGenerator:
    """
    Generates embeddings for document chunks and queries
    """
    
    def __init__(self, model_name: str = None):
        self.model_name = model_name or "text-embedding-ada-002"
        self.model = OpenAIEmbeddings(model=self.model_name)
        
    def embed_chunks_using_openai_embeddings(self, texts: List):
        embedding_vectors = self.model.embed_documents(texts)
        return embedding_vectors
    
    def embed_chunks(self, chunks: List[DocumentChunk]) -> List[Embedding]:
        """ Convert document chunks to embeddings """
        log.set_logger("embed_chunks", f"Embedding each chunk using model: '{self.model_name}'", action="info")
        start_time = time.time()
        
        texts = [chunk.content for chunk in chunks]
        embedding_vectors = self.embed_chunks_using_openai_embeddings(texts)
        
        embeddings = []
        for idx, chunk in enumerate(chunks):
            embedding = Embedding(
                id=str(uuid.uuid4()),
                chunk_id=chunk.id,
                document_id=chunk.document_id,
                embedding_vector=embedding_vectors[idx],
                model_name=self.model_name,
                metadata=chunk.metadata
            )
            embeddings.append(embedding)
            
        elapsed_time = time.time() - start_time
        log.set_logger(
            "embed_chunks",
            f"✅ Embedded {len(texts)} chunks using model '{self.model_name}' in '{elapsed_time:.2f} seconds'.",
            action="info"
        )
        return embeddings
    
    def embed_query(self, query: Union[str, Query]) -> List[float]:
        """Convert a query to embedding vector"""
        
        if isinstance(query, str):
            query_text = query
        else:
            query_text = query.query_text
                    
        # for using OpenAIEmbedding
        embedding_vector = self.model.embed_query(query_text)
        
        return embedding_vector 
    