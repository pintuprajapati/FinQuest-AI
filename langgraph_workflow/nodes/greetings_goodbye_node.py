import logging
from langgraph_workflow.models import WorkflowState
from utils import create_response
from langgraph_workflow.prompt_templates.nodes_prompts import greetings_prompt
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o", temperature=0.4)
logger = logging.getLogger(__name__)


async def greetings_and_goodbye_node(state: WorkflowState):
    """ Greeet or say Goodbye based on user query """
    try:
        logger.info("\n################### NODE: greetings_and_goodbye_node ###################")
        
        history = state.get("messages")[-3:] if state.get("messages") else "" # get last n messaages
        logger.debug(f"User messages history: {history}")
        
        last_intent = state.get("last_intent") if state.get("last_intent") else "" # get last n messaages
        logger.debug(f"User's previous query's intent: {last_intent}")
        
        question = state["question"] # current user query
        
        # for reference: https://python.langchain.com/docs/integrations/chat/openai/
        chain = greetings_prompt | llm
        
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
        logger.error(f"Error processing document: {str(e)}")
        raise e
    