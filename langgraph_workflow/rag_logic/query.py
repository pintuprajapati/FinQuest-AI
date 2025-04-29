import logging
from fastapi import Query
from typing import List
from langchain_openai import ChatOpenAI
from langchain_openai.embeddings import OpenAIEmbeddings
from langgraph_workflow.rag_logic.quadrant_client_wrapper import QuadrantWrapper
from langgraph_workflow.models import SearchResult
from langgraph_workflow.utils import synthesize_rag_answer

llm = ChatOpenAI(model="gpt-4o", temperature=0.4)
logger = logging.getLogger(__name__)

embedding_model = OpenAIEmbeddings(model="text-embedding-ada-002")
quadrant = QuadrantWrapper()

async def query_rag(user_question: str) -> str:
    """ Query the document from vector db based on user query """
    try:
        logger.info(f"User query in query_rag: {user_question}")
        
        # get embeddings for user query
        query_vector = embedding_model.embed_query(user_question)
        
        # fetch top chunks from quadrant
        chunks = quadrant.query_quadrant(query_vector, top_k=5, collection_name="Book")
        
        # Format content into context
        context = "\n\n".join([chunk.content for chunk in chunks if chunk.content])      
        
        if not context:
            logger.debug(f"context: {context}")
            logger.debug("I'm sorry, I couldn't find any relevant information.")
            return "I'm sorry, I couldn't find any relevant information."
        
        rag_response = await synthesize_rag_answer(user_question, context)

        return rag_response
    except Exception as e:
        logger.error(f"Exception: {str(e)}")
        return "An error occurred while fetching the answer."
