import logging
from fastapi import APIRouter, Depends
from typing import List, Dict, Any
from utils import create_response
import os
from langgraph_workflow.models import ChatRequest
from langgraph_workflow.workflow import LanggraphAgents

router = APIRouter(prefix="/agent", tags=["agent"])

lang_agent = LanggraphAgents()
logger = logging.getLogger(__name__)

@router.post("/chat")
async def chat(request: ChatRequest, graph=Depends(lang_agent.build_workflow)):
    try:
        logger.info("========= Inside Chat API =========")
        logger.debug(f"User query: {request.question}")
        
        intial_state = {
            "question": request.question
        }
        
        result_state = await graph.ainvoke(input=intial_state)
        
        logger.debug(f"Answer for the user query: {result_state.get('answer')}")
        return create_response(message="Answer retrieved successfully", status_code=200, success=True, data=f"{result_state.get('answer')}")
    except Exception as e:
        logger.error(f"Error processing document: {str(e)}")
        return create_response(message="Something went wrong while retrieving the answer", status_code=500, success=False, data={})
