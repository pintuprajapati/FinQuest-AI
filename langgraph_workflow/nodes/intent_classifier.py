import logging
from langgraph_workflow.models import WorkflowState
from utils import create_response
from langgraph_workflow.prompt_templates.nodes_prompts import intent_classifier_prompt
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o", temperature=0.4)
logger = logging.getLogger(__name__)


async def intent_classifier_node(state: WorkflowState):
    """ Classify the intent based on user query """
    try:
        logger.info("\n################### NODE: intent_classifier_node ###################")
        logger.info("Classifying the intent based on user query...")
        
        history = state.get("messages")[-5:] if state.get("messages") else "" # get last n messaages
        logger.debug(f"User messages history: {history}")
        
        question = state["question"] # current user query
        
        # for reference: https://python.langchain.com/docs/integrations/chat/openai/
        chain = intent_classifier_prompt | llm
        
        llm_response = await chain.ainvoke({
            "chat_history": history,
            "current_query": question
        })
        logger.debug(f"LLM Response: {llm_response}")
        
        state['intent'] = llm_response
        logger.debug(f"Final state: {state}\n")
        
        return state
    except Exception as e:
        logger.error(f"Error processing document: {str(e)}")
        raise e
    