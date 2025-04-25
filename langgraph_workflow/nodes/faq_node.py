import logging
from langgraph_workflow.models import WorkflowState
from utils import create_response
from langchain_openai import ChatOpenAI
from langchain.chains.llm import LLMChain

llm = ChatOpenAI(model="gpt-4o", temperature=0.4)
logger = logging.getLogger(__name__)


async def faq_node(state: WorkflowState):
    """ FAQ Node for Frequently Asked Questions """
    try:
        logger.info("\n################### NODE: faq_node ###################")
        
        print("-------- this is FAQ Answer --------")
        state['last_intent'] = state.get("intent")
        state['intent'] = 'faq'
        return state
        
    except Exception as e:
        logger.error(f"Exception in faq node: {str(e)}")
        raise e
    