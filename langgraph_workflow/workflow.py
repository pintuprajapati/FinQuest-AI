from langgraph.graph import END, StateGraph
from pydantic import BaseModel
from typing import Dict, Any, Optional
from langgraph_workflow.models import WorkflowState
from langgraph_workflow.nodes.llm_node import llm_node

# Workflow builder
class LanggraphAgents:
    def __init__(self):
        self.workflow = None
        # self.build_workflow()
    
    def build_workflow(self):
        try:
            workflow = StateGraph(WorkflowState)
            
            # Add nodes
            workflow.add_node("llm_node", llm_node)
            
            # Define edges
            workflow.add_edge("llm_node", END)
            
            workflow.set_entry_point("llm_node")
            
            
            self.workflow = workflow.compile()
            return self.workflow
        except Exception as e:
            print('➡ error in build workflow:', e)
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
        