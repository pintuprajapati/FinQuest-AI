from langgraph_workflow.models import WorkflowState
from utils import create_response
import custom_log as log

async def llm_node(state: WorkflowState):
    try:
        log.set_logger("llm_node", f"Getting answer from llm node...", action="info")
        state['answer'] = "answer from llm node"
        return state
    except Exception as e:
        log.set_logger("llm_node", f"Error processing document: {str(e)}", action="error")
        raise e
    