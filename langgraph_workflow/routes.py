from fastapi import APIRouter, Depends
from typing import List, Dict, Any
from utils import create_response
import custom_log as log
import os
from langgraph_workflow.models import ChatRequest
from langgraph_workflow.workflow import LanggraphAgents

router = APIRouter(prefix="/agent", tags=["agent"])

lang_agent = LanggraphAgents()

@router.post("/chat")
async def chat(request: ChatRequest, graph=Depends(lang_agent.build_workflow)):
    try:
        log.set_logger("chat", f"========= Inside Chat API =========", action="info")
        intial_state = {
            "question": request.question
        }
        
        result_state = await graph.ainvoke(input=intial_state)
        
        log.set_logger("chat", f"Answer for the query: ", action="info")
        return create_response(message="Answer retrieved successfully", status_code=200, success=True, data={})
    except Exception as e:
        log.set_logger("chat", f"Error processing document: {str(e)}", action="error")
        return create_response(message="Something went wrong while retrieving the answer", status_code=500, success=False, data={})
