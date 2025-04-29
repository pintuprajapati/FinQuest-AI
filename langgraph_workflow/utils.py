import logging
from fastapi import Query
from typing import List
from langchain_openai import ChatOpenAI
from langchain_openai.embeddings import OpenAIEmbeddings
from langgraph_workflow.rag_logic.quadrant_client_wrapper import QuadrantWrapper
from langgraph_workflow.models import SearchResult
from langgraph_workflow.prompt_templates import general_prompts

llm = ChatOpenAI(model="gpt-4o", temperature=0.4)
logger = logging.getLogger(__name__)

async def synthesize_rag_answer(context: str, user_question: str) -> str:
    """
    Uses an LLM to synthesize an answer from provided context and user question.
    If context is not relevant, returns a fallback response.
    """
    try:
        # for reference: https://python.langchain.com/docs/integrations/chat/openai/
        chain = general_prompts.rag_prompt | llm
        
        llm_response = await chain.ainvoke({
            "context": context,
            "user_question": user_question
        })
        
        logger.debug(f"Synthesized RAG Response: {llm_response.content}")
        # logger.debug(f"Synthesized RAG Response: {llm_response}")
        
        return llm_response.content
    except Exception as e:
        logger.error(f"Exception: {str(e)}")
        raise e
    