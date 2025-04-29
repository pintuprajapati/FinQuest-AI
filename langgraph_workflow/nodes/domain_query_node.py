import logging
from langgraph_workflow.models import WorkflowState
from utils import create_response
from langgraph_workflow.prompt_templates.nodes_prompts import domain_query_prompt
from langchain_openai import ChatOpenAI
from langchain.chains.llm import LLMChain
from langgraph_workflow.rag_logic.query import query_rag

llm = ChatOpenAI(model="gpt-4o", temperature=0.4)
logger = logging.getLogger(__name__)


async def domain_query_node(state: WorkflowState):
    """ FAQ Node for Frequently Asked Questions """
    try:
        logger.info("\n################### NODE: math_node ###################")
        
        history = state.get("messages")[-3:] if state.get("messages") else "" # get last n messaages
        logger.debug(f"User messages history: {history}")
        
        last_intent = state.get("last_intent") if state.get("last_intent") else "" # get last n messaages
        logger.debug(f"User's previous query's intent: {last_intent}")
        
        question = state["question"] # current user query
        
        rag_answer = await query_rag(question)
        
        state['last_intent'] = state.get('intent') or ""
        state['answer'] = rag_answer
        logger.debug(f"Final state: {state}\n")
        
        return state        
    except Exception as e:
        logger.error(f"Exception: {str(e)}")
        raise e
