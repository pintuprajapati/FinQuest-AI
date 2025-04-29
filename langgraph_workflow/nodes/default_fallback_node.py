import logging
from langgraph_workflow.models import WorkflowState
from utils import create_response
from langchain_openai import ChatOpenAI
from langchain.chains.llm import LLMChain

llm = ChatOpenAI(model="gpt-4o", temperature=0.4)
logger = logging.getLogger(__name__)


async def default_fallback_node(state: WorkflowState):
    """ FAQ Node for Frequently Asked Questions """
    try:
        logger.info("\n################### NODE: default_fallback_node ###################")
        
        print("-------- this is DEFAULT FALLBACK NODE Answer --------")
        state['last_intent'] = state.get("intent")
        state['intent'] = 'other'
        return state
        
    except Exception as e:
        logger.error(f"Exception in default_fallback_node: {str(e)}")
        raise e
    