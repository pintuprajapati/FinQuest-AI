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
# from qdrant_client import AsyncQdrantClient, models
from qdrant_client import QdrantClient, models
import numpy as np
import custom_log as log

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
        
        # Create collection if it doesn't exist (for chroma db)
        self.collection = self.client.get_or_create_collection("document_embeddings")
        
        self.quadrant_client = QdrantClient(host="localhost", port=6333)
        self.collection_name = ""
        
    async def add_embeddings_to_quadrant(self, embeddings: List[Embedding], chunks: List[DocumentChunk], collection_name: str = None):
        """ Add embeddings to the quadrant vector db """
        
        collection_name = collection_name or self.collection_name
        if not self.quadrant_client.collection_exists(collection_name):
            log.set_logger("add_embeddings_to_quadrant", f"New collection '{collection_name}' will be created", action="info")
            self.quadrant_client.create_collection(
                collection_name=collection_name,
                vectors_config=models.VectorParams(size=1536, distance=models.Distance.COSINE),
            )
        else:
            log.set_logger("add_embeddings_to_quadrant", f"Collection '{collection_name}' exists already", action="info")
        
        # Insert vectors into a collection
        log.set_logger("add_embeddings_to_quadrant", f"Data is being inserted to the collection: '{collection_name}'", action="info")
        operation_info = self.quadrant_client.upsert(
            collection_name=collection_name,
            wait=True,
            points=[
                models.PointStruct(
                    id=idx,
                    vector=embedding.embedding_vector,
                     payload={
                        **embedding.metadata, # Include metadata from Embedding
                        "chunk_id": embedding.chunk_id,
                        "document_id": embedding.document_id,
                        "model_name": embedding.model_name,
                        "created_at": embedding.created_at.isoformat()
                    }
                )
                for idx, embedding in enumerate(embeddings)
            ],
        )
        log.set_logger("add_embeddings_to_quadrant", f"Operation Info (data ingestion status): '{operation_info}'", action="info")
        
        # Check the collection size to make sure all the points have been stored
        collection_size = self.quadrant_client.count(collection_name=collection_name)
        log.set_logger("add_embeddings_to_quadrant", f"collection_size: '{collection_size}'", action="info")
        
    async def add_embeddings_to_chroma(self, embeddings: List[Embedding], chunks: List[DocumentChunk]):
        """ Add embeddings to the chroma vector db """
        
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
    
    async def add_embeddings(self, embeddings: List[Embedding], chunks: List[DocumentChunk]) -> None:
        """Add document embeddings to vector store"""
        log.set_logger("add_embeddings", f"Embeddings will be added to vector db", action="info")
        
        collection_name = "Book" # static collection name for now
        await self.add_embeddings_to_quadrant(embeddings, chunks, collection_name)
        # self.add_embeddings_to_chroma(embeddings, chunks)
        
        log.set_logger("add_embeddings", f"Embeddings have been added to vector db", action="info")
    
    async def query_quadrant(self, query_embedding: List[float], top_k: int = 5, collection_name: str = None) -> List[SearchResult]:
        """ Search for similar documents using vector similarity (from Quadrant Vector DB) """
        
        collection_name = "Book" # static for now
        
        results = self.quadrant_client.search(
            collection_name=collection_name or self.collection_name,
            query_vector=query_embedding,
            with_payload=True,
            limit=top_k
        )
        log.set_logger("query_quadrant", f"Results from Quadrant: {results}", action="info")
        
        # Here, results only return the Quadrant Points and payload/metadata
        # But I haven't added any 'text content' in it. so I'm going to use Lnagchain Qudarant and see if it works
        
        search_results = []
        # for i in range(len(results['ids'][0])):
        #     result = SearchResult(
        #         document_id=results['metadatas'][0][i]['document_id'],
        #         chunk_id=results['metadatas'][0][i].get('chunk_id', ''),
        #         content=results['documents'][0][i],
        #         similarity=float(results['distances'][0][i]) if 'distances' in results else 0.0,
        #         metadata=results['metadatas'][0][i]
        #     )
        #     search_results.append(result)
            
        return search_results 
        
    def search(self, query_embedding: List[float], top_k: int = 5) -> List[SearchResult]:
        """ Search for similar documents using vector similarity """
        
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