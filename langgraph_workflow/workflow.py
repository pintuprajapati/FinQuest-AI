import logging
from langgraph.graph import END, StateGraph
from pydantic import BaseModel
from typing import Dict, Any, Optional
from langgraph_workflow.models import WorkflowState
from langgraph_workflow.nodes import (
    greetings_goodbye_node,
    intent_classifier_node,
    faq_node,
    routing_node,
    llm_node
)
from langchain_openai import ChatOpenAI
logger = logging.getLogger(__name__)

# Workflow builder
class LanggraphAgents:
    def __init__(self):
        self.workflow = None
        # self.build_workflow()
        self.openai_llm = ChatOpenAI(model="gpt-4o", temperature=0.4)
    
    def build_workflow(self):
        try:
            workflow = StateGraph(WorkflowState)
            
            # Create and add intent node
            
            # Add nodes
            workflow.add_node("intent_classifier_node", intent_classifier_node.intent_classifier_node)
            workflow.add_node("greeting_and_goodbye_node", greetings_goodbye_node.greetings_and_goodbye_node)
            workflow.add_node("faq_node", faq_node.faq_node)
            
            workflow.add_conditional_edges(
                "intent_classifier_node",
                routing_node.routing_node,
                {
                    "greeting": "greeting_and_goodbye_node",
                    "goodbye": "greeting_and_goodbye_node",
                    "faq": "faq_node"
                }                
            )
            
            # Add end nodes
            workflow.add_edge("greeting_and_goodbye_node", END)
            workflow.add_edge("faq_node", END)
            
            # Define conditional edges
            workflow.set_entry_point("intent_classifier_node")
            
            self.workflow = workflow.compile()
            return self.workflow
        except Exception as e:
            logger.error(f"Exception in build workflow: {str(e)}")
            raise e
    
    async def workflow_kickoff(self, user_input: Dict) -> Dict:
        try:
            print("=== Starting LangGraph Workflow ===")
            # Initialize state with user input
            initial_state = WorkflowState(input=user_input)
            
            # Execute workflow
            return await self.workflow.ainvoke(initial_state)
            
        except Exception as e:
            print(f"Workflow error: {e}")
            return {"status": "error", "message": str(e)}
        