import logging
from langgraph_workflow.models import WorkflowState
from utils import create_response
from langgraph_workflow.prompt_templates.nodes_prompts import intent_classifier_prompt
from langchain_openai import ChatOpenAI
from langchain.chains.llm import LLMChain
from langgraph_workflow.config import langgraph_routing_nodes

llm = ChatOpenAI(model="gpt-4o", temperature=0.4)
logger = logging.getLogger(__name__)


async def routing_node(state: WorkflowState):
    """ Route the node accordingly based on classified intent """
    try:
        logger.info("\n################### NODE: routing_node ###################")
        
        state['last_intent'] = state.get("intent")
        current_intent = state.get("intent") or "default_fallback_node" # get current intent
        logger.info(f"current_intent: '{current_intent}'")
        logger.info(f"User query will be routed to '{langgraph_routing_nodes.get(current_intent)}'....")
        
        
        ## update the state and return as tuple
        # return state, current_intent
    
        return current_intent
        
    except Exception as e:
        logger.error(f"Exception: {str(e)}")
        raise e
