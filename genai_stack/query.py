from typing import List, Dict, Any
from models.query import Query, SearchResult
from .embedding import EmbeddingGenerator
from .vector_storage import VectorStore
from langchain_openai import ChatOpenAI
import logging

logger = logging.getLogger(__name__)

class QueryProcessor:
    """
    Processes user queries and retrieves relevant information
    """
    
    def __init__(self, embedding_generator: EmbeddingGenerator, vector_store: VectorStore):
        self.embedding_generator = embedding_generator
        self.vector_store = vector_store
        self.openai_llm = ChatOpenAI(model="gpt-4o", temperature=0.4)
    
    async def process_query(self, query_text: str, top_k: int = 5) -> List[SearchResult]:
        """Process a user query and return relevant document chunks"""
        try:
            logger.info(f"Processing user query")
            # Create query object
            query = Query(query_text=query_text)
            
            # Convert query to embedding
            query_embedding = self.embedding_generator.embed_query(query)
            query.embedding_vector = query_embedding
            
            # Search vector database
            # search_results = self.vector_store.search(query_embedding, top_k=top_k)
            search_results = await self.vector_store.query_quadrant(query_embedding, top_k=top_k)
            
            return search_results
        except Exception as e:
            logger.error(f"Some error occurred")
            raise e
    
    def format_response(self, search_results: List[SearchResult]) -> str:
        """Format search results into a coherent response"""
        if not search_results:
            return "I couldn't find any relevant information."
        
        response = "Here's what I found:\n\n"
        
        for i, result in enumerate(search_results, 1):
            response += f"{i}. {result.content[:200]}...\n\n"
            
        return response 
    
    async def generate_response(self, query: str, context: List[SearchResult]):
        """ Generate a response using LLM based on user query adn context """
        
        context_str = "\n".join([result.content for result in context])
        
        
        human_prompt = f"""
        Answer the question based on the context below.
        Question: {query}
        Context: {context_str}
        Answer:
        """
        
        messages = [
            (
                "system",
                "You are a helpful assistant that understands user query and context and provide response accordingly",
            ),
            ("human", human_prompt),
        ]
        
        return await self.openai_llm.ainvoke(messages)
    