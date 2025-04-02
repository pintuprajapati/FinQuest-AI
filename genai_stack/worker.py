import os
from celery import Celery
from core.config import settings

# Import AI stack components
from .document import DocumentProcessor
from .chunking import TextChunker
from .embedding import EmbeddingGenerator
from .vector_storage import VectorStore
from models.document import Document, DocumentStatus

# Set up Celery
celery_app = Celery(
    'ai_stack.worker',
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)

# Initialize services
document_processor = DocumentProcessor()
text_chunker = TextChunker()
embedding_generator = EmbeddingGenerator()
vector_store = VectorStore()

@celery_app.task(name="process_document")
def process_document(document_dict: dict):
    """Background task to process document"""
    # Convert dict to Document object
    document = Document(**document_dict)
    
    try:
        # Update status to processing
        document.status = DocumentStatus.PROCESSING
        
        # Extract text from document
        text = document_processor.extract_text(document)
        
        # Chunk the text
        chunks = text_chunker.chunk_text(document, text)
        
        # Generate embeddings
        embeddings = embedding_generator.embed_chunks(chunks)
        
        # Store in vector database
        vector_store.add_embeddings(embeddings, chunks)
        
        # Update document status
        document.status = DocumentStatus.PROCESSED
        
        return {"status": "success", "document_id": document.id}
    
    except Exception as e:
        document.status = DocumentStatus.FAILED
        return {"status": "error", "document_id": document.id, "error": str(e)} 