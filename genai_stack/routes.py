from fastapi import APIRouter, UploadFile, File, BackgroundTasks, HTTPException, Depends, Query, Body
from typing import List, Dict, Any

# Import AI stack components
from genai_stack import DocumentProcessor, TextChunker, EmbeddingGenerator, VectorStore, QueryProcessor
# Import worker functions directly instead of the task
from genai_stack.worker import (
    document_processor as worker_doc_processor,
    text_chunker as worker_text_chunker,
    embedding_generator as worker_embedding_generator,
    vector_store as worker_vector_store
)
from models.document import Document, DocumentStatus, DocumentProcessRequest
from models.query import SearchResult
from utils import create_response, download_file_to_local, delete_local_file_dir
import custom_log as log
import os
from core.config import settings

router = APIRouter(prefix="/ai", tags=["ai"])

# Initialize AI stack components
document_processor = DocumentProcessor()
text_chunker = TextChunker()
embedding_generator = EmbeddingGenerator()
vector_store = VectorStore()
query_processor = QueryProcessor(embedding_generator, vector_store)

@router.post("/documents/process", response_model=Dict[str, Any])
async def upload_document(request: DocumentProcessRequest):
    """Upload a document for processing"""
    try:
        # Use request.file_url instead of file_url
        file_url = request.file_url
        
        # Download file if it's a URL
        local_file_path = None
        url_prefixes = ('http://', 'https://', 's3://')
        if file_url.startswith(url_prefixes):
            download_dir = os.path.join(settings.STATIC_DIR, 'downloaded_files')
            local_file_path = await download_file_to_local(file_url, download_dir)
            if not local_file_path:
                log.set_logger("upload_document", f"Failed to download file from {file_url}", action="debug")
                return create_response(message=f"Failed to download file from {file_url}", status_code=400, success=False, data={})
        else:
            log.set_logger("upload_document", f"Please provide url which starts from this: {url_prefixes}", action="debug")
            return create_response(message=f"Please provide url which starts from this: {url_prefixes}", status_code=400, success=False, data={})
            
        # Create document from URL
        document = document_processor.create_file_document(local_file_path)
        
        # Process document directly instead of using Celery
        log.set_logger("upload_document", f"Starting document processing for document ID: {document.id}", action="info")
        
        # Update status to processing
        document.status = DocumentStatus.PROCESSING
        
        # Extract text from document
        text = worker_doc_processor.extract_text(document)
        
        # # Chunk the text
        chunks = worker_text_chunker.chunk_text(document, text)
        
        # # Generate embeddings
        embeddings = worker_embedding_generator.embed_chunks(chunks)
        
        # # Store in vector database
        worker_vector_store.add_embeddings(embeddings, chunks)
        
        # # Update document status
        document.status = DocumentStatus.PROCESSED
        
        # Clean up downloaded file if necessary
        delete_local_file_dir(local_file_path)
            
        log.set_logger("upload_document", f"Document processing completed for ID: ", action="info")
        
        result_data = {
            "document_id": document.id,
            "status": document.status
        }
        
        log.set_logger("upload_document", f"Document is being processed. Please wait..", action="info")
        return create_response(message="Document is being processed. Please wait..", status_code=200, success=True, data=result_data)
    except Exception as e:
        log.set_logger("upload_document", f"Error processing document: {str(e)}", action="error")
        return create_response(message="Something went wrong while processing the document", status_code=500, success=False, data={})

@router.post("/documents/upload", response_model=Dict[str, Any])
async def upload_document(file: UploadFile = File(...)):
    """Upload a document for processing"""
    try:
        document = await document_processor.upload_document(file)
        
        # Start processing task in background
        # process_document.delay(document.dict())
        
        result_data = {
            "document_id": document.id
        }
        
        log.set_logger("upload_document", f"Document uploaded and queued for processing", action="info")
        return create_response(message="Document uploaded and queued for processing", status_code=200, success=True, data=result_data)
    except Exception as e:
        log.set_logger("upload_document", f"Error uploading document: {str(e)}", action="error")
        return create_response(message="Something went wrong while uploading a document", status_code=500, success=False, data={})

@router.get("/query", response_model=Dict[str, Any])
async def query_documents(q: str = Query(..., description="Query text"), top_k: int = Query(5, description="Number of results to return")):
    """Query the document database"""
    try:
        log.set_logger("query", f"User query: {q}", action="info")
        search_results = await query_processor.process_query(q, top_k=top_k)
        response = query_processor.format_response(search_results)
        
        result_data = {
            "query": q,
            "results": [result.dict() for result in search_results],
            "response": response
        } 
        
        log.set_logger("query", f"Result fetched successfully", action="info")
        return create_response(message="Result fetched successfully", status_code=200, success=True, data=result_data)
    except Exception as e:
        log.set_logger("query", f"Error while getting the result for the query: {str(e)}", action="error")
        return create_response(message="Something went wrong while getting answer for the query", status_code=500, success=False, data={})