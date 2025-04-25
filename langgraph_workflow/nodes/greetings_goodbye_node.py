import logging
from langgraph_workflow.models import WorkflowState
from utils import create_response
from langgraph_workflow.prompt_templates.nodes_prompts import intent_classifier_prompt
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o", temperature=0.4)
logger = logging.getLogger(__name__)


async def greetings_and_goodbye_node(state: WorkflowState):
    """ Greeet or say Goodbye based on user query """
    try:
        logger.info("\n################### NODE: greetings_and_goodbye_node ###################")
     
        
        print("----------Hi greeting form node------")
        return state
    except Exception as e:
        logger.error(f"Error processing document: {str(e)}")
        raise e
    