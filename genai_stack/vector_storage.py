### Chorma db ###
# RuntimeError: Your system has an unsupported version of sqlite3. Chroma requires sqlite3 >= 3.35.0.
# If you face above chromadb error, then install the 'pysqlite3-binary' and add below code in the file where you are importing chromadb
# Install this lib first: pip install pysqlite3-binary

__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import os
from typing import List, Dict, Any, Optional
import chromadb
from chromadb.config import Settings
import uuid

from models.document import DocumentChunk
from models.embeddings import Embedding
from models.query import SearchResult
from core.config import settings

class VectorStore:
    """
    Manages storage and retrieval of vector embeddings
    """
    
    def __init__(self, persist_directory: str = None):
        self.persist_directory = persist_directory or settings.VECTOR_DB_PATH
        os.makedirs(self.persist_directory, exist_ok=True)
        
        # Initialize ChromaDB
        self.client = chromadb.PersistentClient(
            path=self.persist_directory,
            settings=Settings(anonymized_telemetry=False)
        )
        
        # Create collection if it doesn't exist
        self.collection = self.client.get_or_create_collection("document_embeddings")
    
    def add_embeddings(self, embeddings: List[Embedding], chunks: List[DocumentChunk]) -> None:
        """Add document embeddings to vector store"""
        ids = [embedding.id for embedding in embeddings]
        embedding_vectors = [embedding.embedding_vector for embedding in embeddings]
        metadatas = [
            {
                "document_id": embedding.document_id,
                "chunk_id": embedding.chunk_id,
                **embedding.metadata
            } 
            for embedding in embeddings
        ]
        documents = [chunk.content for chunk in chunks]
        
        self.collection.add(
            ids=ids,
            embeddings=embedding_vectors,
            metadatas=metadatas,
            documents=documents
        )
    
    def search(self, query_embedding: List[float], top_k: int = 5) -> List[SearchResult]:
        """Search for similar documents using vector similarity"""
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        
        search_results = []
        for i in range(len(results['ids'][0])):
            result = SearchResult(
                document_id=results['metadatas'][0][i]['document_id'],
                chunk_id=results['metadatas'][0][i].get('chunk_id', ''),
                content=results['documents'][0][i],
                similarity=float(results['distances'][0][i]) if 'distances' in results else 0.0,
                metadata=results['metadatas'][0][i]
            )
            search_results.append(result)
            
        return search_results 