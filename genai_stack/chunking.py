import uuid
import json
from typing import List, Dict, Any

from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document as LangchainDocument

from models.document import Document, DocumentChunk
from core.config import settings
import custom_log as log
from utils import parse_llm_response
import genai_stack.general_prompts as general_prompts
import asyncio

class TextChunker:
    """
    Handles text chunking and metadata enrichment for document processing.
    """

    def __init__(self, chunk_size: int = None, chunk_overlap: int = None):
        self.chunk_size = chunk_size or settings.CHUNK_SIZE
        self.chunk_overlap = chunk_overlap or settings.CHUNK_OVERLAP

        self.embedding_model = OpenAIEmbeddings()
        self.openai_llm = ChatOpenAI(model="gpt-4o", temperature=0.4)

        self.semantic_text_splitter = SemanticChunker(
            embeddings=self.embedding_model,
            breakpoint_threshold_type="percentile",
            breakpoint_threshold_amount=0.98
        )

    async def chunk_text(self, document: Document, text: str) -> List[DocumentChunk]:
        """
        Split document text into overlapping chunks of fixed size.
        """
        step = max(1, self.chunk_size - self.chunk_overlap)
        chunks = []

        for i in range(0, len(text), step):
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

    def merge_short_chunks(self, docs: List[LangchainDocument]) -> List[str]:
        """
        Merge consecutive text chunks with fewer than 300 characters.
        """
        MIN_CHUNK_LEN = 300
        merged_chunks = []
        buffer = ""

        for doc in docs:
            chunk = doc.page_content.strip()
            if len(buffer) + len(chunk) < MIN_CHUNK_LEN:
                buffer += " " + chunk
            else:
                if buffer:
                    merged_chunks.append(buffer.strip())
                buffer = chunk
        if buffer:
            merged_chunks.append(buffer.strip())

        return merged_chunks

    async def enrich_chunk(self, prompt_template, chunk):
        prompt = prompt_template.format_messages(chunk=chunk)
        try:
            response = await self.openai_llm.ainvoke(prompt)
            metadata = parse_llm_response(response.content)
        except Exception as e:
            log.set_logger("metadata_enrichment", f"Failed to enrich chunk: {e}", action="error")
            metadata = {"title": "", "theme": "", "tags": []}
        return {
            "chunk": chunk,
            "title": metadata.get("title", "").strip(),
            "theme": metadata.get("theme", "").strip(),
            "tags": metadata.get("tags", [])
        }
            
    async def add_metadata_to_chunk(self, merged_chunks: List[str]) -> List[Dict[str, Any]]:
        """
        Enrich each text chunk with metadata using an LLM.
        """
        prompt_template = ChatPromptTemplate.from_template(
            general_prompts.chunking_metadata_prompt_template
        )

        results = await asyncio.gather(*(self.enrich_chunk(prompt_template, chunk) for chunk in merged_chunks))
        return results

    async def semantic_chunking_by_langchain(self, document: Document, text: str) -> List[str]:
        """
        Perform semantic chunking using LangChain's SemanticChunker.
        """
        log.set_logger("semantic_chunking_by_langchain", "Inside semantic chunking process", action="info")

        lines = [line.strip() for line in text.splitlines() if line.strip()]
        docs = self.semantic_text_splitter.create_documents(lines)
        merged_chunks = self.merge_short_chunks(docs)
        
        enriched_chunks = await self.add_metadata_to_chunk(merged_chunks)

        return enriched_chunks
