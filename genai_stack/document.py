import os
import shutil
import uuid
from typing import List, Dict, Any
from fastapi import UploadFile
from urllib.parse import urlparse

# Document extraction libraries
import pypdf
import docx2txt
# import pymupdf
# import fitz  # PyMuPDF
import pymupdf4llm
import pathlib
import time

from models.document import Document, DocumentType, DocumentStatus
from core.config import settings
import custom_log as log
import utils

class DocumentProcessor:
    """
    Handles document upload and text extraction
    """
    
    def __init__(self):
        os.makedirs(settings.STATIC_DIR, exist_ok=True)
    
    async def upload_document(self, file: UploadFile) -> Document:
        """Upload and save a document file"""
        file_extension = file.filename.split(".")[-1].lower()
        document_type = self._get_document_type(file_extension)
        
        # Generate unique ID and path
        doc_id = str(uuid.uuid4())
        file_path = os.path.join(settings.STATIC_DIR, f"{doc_id}.{file_extension}")
        
        # Save the file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Create document record
        document = Document(
            id=doc_id,
            filename=file.filename,
            file_path=file_path,
            document_type=document_type,
            status=DocumentStatus.PENDING,
            metadata={"size": os.path.getsize(file_path)}
        )
        
        return document
    
    def create_file_document(self, filepath: str) -> Document:
        """ 
        Take the file data from filepath and create a Document record
        """

        filename = filepath.split("/")[-1] # extract filename.ext
        file_extension = filename.split(".")[-1] # split 'filename' and 'ext'
        document_type = self._get_document_type(file_extension)
        
        # Generate unique ID and path
        doc_id = str(uuid.uuid4())
        
        # Create document record
        document = Document(
            id=doc_id,
            filename=filename,
            file_path=filepath,
            document_type=document_type,
            status=DocumentStatus.PENDING,
            metadata={"size": os.path.getsize(filepath)}            
        )
        
        return document
        
    def extract_text(self, document: Document) -> str:
        """Extract text from various document types"""
        if document.document_type == DocumentType.PDF:
            result, filepath = self._extract_from_pdf(document.file_path, document.id)
            return result, filepath
        elif document.document_type == DocumentType.DOCX:
            return self._extract_from_docx(document.file_path)
        elif document.document_type == DocumentType.TXT:
            return self._extract_from_txt(document.file_path)
        elif document.document_type == DocumentType.IMAGE:
            return self._extract_from_img(document.file_path)
        elif document.document_type == DocumentType.AUDIO:
            return self._extract_from_audio(document.file_path)
        else:
            raise ValueError(f"Unsupported document type: {document.document_type}")
    
    def extract_using_pymupdf(self, file_path: str, doc_id: str):
        """ Extract the data into markdown format (including tables, multi-columns and indexes) """
        
        start_time = time.time()
        
        md_text = pymupdf4llm.to_markdown(file_path)
        
        static_file_dir = os.path.join(settings.STATIC_DIR, 'md_files')
        utils.create_local_dir(static_file_dir)
        
        # Create file path with doc_id
        md_filepath = os.path.join(static_file_dir, f"{doc_id}.md")
        
        # Save extracted text to a md file
        pathlib.Path(md_filepath).write_bytes(md_text.encode())
        
        log.set_logger("extract_using_pymupdf", f"Extracted text saved to the md file: '{md_filepath}'", action="info")
        
        log.set_logger("extract_using_pymupdf", f"Total time elapsed while extracting text: {time.time() - start_time}", action="info")
        
        return md_text, md_filepath
        
    def extract_using_pdfreader(self, file_path: str, doc_id: str):
        text = ""
        with open(file_path, "rb") as file:
            pdf = pypdf.PdfReader(file)
            for page in pdf.pages:
                text += page.extract_text() + "\n"
        
        static_file_dir = os.path.join(settings.STATIC_DIR, 'text_files')
        utils.create_local_dir(static_file_dir)
        
        # Create file path with doc_id
        text_filepath = os.path.join(static_file_dir, f"{doc_id}.txt")
        
        # Save extracted text to a file
        with open(text_filepath, "w", encoding="utf-8") as f:
            f.write(text)
        
        log.set_logger("_extract_from_pdf", f"Extracted text saved to the file: '{text_filepath}'", action="info")
        
        return text, text_filepath
    
    def _extract_from_pdf(self, file_path: str, doc_id: str) -> str:
        
        return self.extract_using_pymupdf(file_path, doc_id)
    
        # simple text extraction
        # return self.extract_using_pdfreader(file_path, doc_id)
    
    def _extract_from_docx(self, file_path: str) -> str:
        return docx2txt.process(file_path)
    
    def _extract_from_txt(self, file_path: str) -> str:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    
    def _extract_from_img(self, file_path: str) -> str:
        # your code
        pass
    
    def _extract_from_audio(self, file_path: str) -> str:
        # your code
        pass
    
    def _get_document_type(self, extension: str) -> DocumentType:
        if extension == "pdf":
            return DocumentType.PDF
        elif extension in ["docx", "doc"]:
            return DocumentType.DOCX
        elif extension == "txt":
            return DocumentType.TXT
        elif extension in ("png", "jpg", "jpeg", "webp"):
            return DocumentType.IMAGE
        elif extension in ("mp3", "wav", "aac", "flac", "ogg", "m4a"):
            return DocumentType.AUDIO
        else:
            return DocumentType.OTHER 