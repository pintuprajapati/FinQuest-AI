from fastapi import APIRouter, Request
from api.schemas import SearchSchema
from api import crud
import logging
logger = logging.getLogger(__name__)

router = APIRouter(tags=["Search"])

@router.post("/search")
async def search(request: Request, request_body: SearchSchema):
    """ Search API to get the relevant results based on user query """
    logger.info(f"=== Inside search api ===")    
    search_results = await crud.get_search_results(request_body)
    return search_results
    

