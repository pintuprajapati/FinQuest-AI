from langgraph.graph import END, StateGraph
from pydantic import BaseModel
from typing import Dict, Any, Optional
from langgraph_workflow.models import WorkflowState
from langgraph_workflow.nodes import (
    intent_classifier,
    llm_node
)
from langchain_openai import ChatOpenAI
import custom_log as log

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
            workflow.add_node("intent_classifier_node", intent_classifier.intent_classifier_node)
            
            # Define edges
            workflow.add_edge("intent_classifier_node", END)
            
            workflow.set_entry_point("intent_classifier_node")
            
            self.workflow = workflow.compile()
            return self.workflow
        except Exception as e:
            log.set_logger("build_workflow", f"Exception in build workflow: {str(e)}", action="info")
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
        