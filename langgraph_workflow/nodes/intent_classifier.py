from langgraph_workflow.models import WorkflowState
from utils import create_response
import custom_log as log
from langgraph_workflow.prompt_templates.nodes_prompts import intent_classifier_prompt
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o", temperature=0.4)


async def intent_classifier_node(state: WorkflowState):
    """ Classify the intent based on user query """
    try:
        log.set_logger("intent_classifier_node", f"\n################### NODE: intent_classifier_node ###################", action="info")       
        log.set_logger("intent_classifier_node", f"Classifying the intent based on user query...", action="info")       
        
        history = state.get("messages")[-5:] if state.get("messages") else "" # get last n messaages
        log.set_logger("intent_classifier_node", f"User messages history: {history}", action="info")
        
        question = state["question"] # current user query
        
        # for reference: https://python.langchain.com/docs/integrations/chat/openai/
        chain = intent_classifier_prompt | llm
        
        llm_response = await chain.ainvoke({
            "chat_history": history,
            "current_query": question
        })
        log.set_logger("intent_classifier_node", f"LLM Response: {llm_response}", action="info")
        
        state['intent'] = llm_response
        log.set_logger("intent_classifier_node", f"Final state: {state}\n", action="info")
        
        return state
    except Exception as e:
        log.set_logger("llm_node", f"Error processing document: {str(e)}", action="error")
        raise e
    