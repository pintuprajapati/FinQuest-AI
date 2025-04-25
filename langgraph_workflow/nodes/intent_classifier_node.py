import logging
from langgraph_workflow.models import WorkflowState
from utils import create_response
from langgraph_workflow.prompt_templates.nodes_prompts import intent_classifier_prompt
from langgraph_workflow.config import intent_classication_list
from langchain_openai import ChatOpenAI
import uuid

llm = ChatOpenAI(model="gpt-4o", temperature=0.4)
logger = logging.getLogger(__name__)


async def intent_classifier_node(state: WorkflowState):
    """ Classify the intent based on user query """
    try:
        logger.info("\n################### NODE: intent_classifier_node ###################")
        logger.info("Classifying the intent based on user query...")
        
        # initialize JSON file for chat history
        # session_id = uuid.uuid4()
        
        history = state.get("messages")[-5:] if state.get("messages") else "" # get last n messaages
        logger.debug(f"User messages history: {history}")
        
        last_intent = state.get("last_intent") if state.get("last_intent") else "" # get last n messaages
        logger.debug(f"User's previous query's intent: {last_intent}")
        
        question = state["question"] # current user query
        
        # file_path = f"ai_agent/session_db/{sessionID}.json"
        
        # for reference: https://python.langchain.com/docs/integrations/chat/openai/
        chain = intent_classifier_prompt | llm
        
        llm_response = await chain.ainvoke({
            "intent_classication_list": intent_classication_list,
            "chat_history": history,
            "current_query": question,
            "last_intent": last_intent
        })
        logger.debug(f"LLM Response: {llm_response}")
        
        state['last_intent'] = state.get('intent') or ""
        state['intent'] = llm_response.content
        logger.debug(f"Final state: {state}\n")
        
        return state
    except Exception as e:
        logger.error(f"Error processing document: {str(e)}")
        raise e
    