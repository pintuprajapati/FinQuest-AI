import logging
from langgraph_workflow.models import WorkflowState
from utils import create_response
from langgraph_workflow.prompt_templates.nodes_prompts import fallback_prompt

from langchain_openai import ChatOpenAI
from langchain.chains.llm import LLMChain

llm = ChatOpenAI(model="gpt-4o", temperature=0.4)
logger = logging.getLogger(__name__)


async def default_fallback_node(state: WorkflowState):
    """ FAQ Node for Frequently Asked Questions """
    try:
        logger.info("\n################### NODE: default_fallback_node ###################")
        
        history = state.get("messages")[-3:] if state.get("messages") else "" # get last n messaages
        logger.debug(f"User messages history: {history}")
        
        last_intent = state.get("last_intent") if state.get("last_intent") else "" # get last n messaages
        logger.debug(f"User's previous query's intent: {last_intent}")
        
        question = state["question"] # current user query
        
        # for reference: https://python.langchain.com/docs/integrations/chat/openai/
        chain = fallback_prompt | llm
        
        llm_response = await chain.ainvoke({
            "chat_history": history,
            "current_query": question
        })
        logger.debug(f"LLM Response: {llm_response.content}")
        # logger.debug(f"Full LLM Response: {llm_response}")
        
        state['last_intent'] = state.get('intent') or ""
        state['answer'] = llm_response.content
        logger.debug(f"Final state: {state}\n")
        return state
        
    except Exception as e:
        logger.error(f"Exception: {str(e)}")
        raise e
    