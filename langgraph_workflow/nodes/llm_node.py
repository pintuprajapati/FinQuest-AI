import logging
from langgraph_workflow.models import WorkflowState
from utils import create_response
logger = logging.getLogger(__name__)

async def llm_node(state: WorkflowState):
    try:
        logger.info(f"Getting answer from llm node...")    
        state['answer'] = "answer from llm node"
        return state
    except Exception as e:
        logger.error(f"Error processing document: {str(e)}")
        raise e
    