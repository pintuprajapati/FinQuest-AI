from fastapi import APIRouter, Request
from api.schemas import SearchSchema
from api import crud
import custom_log as log

router = APIRouter(tags=["Search"])

@router.post("/search")
async def search(request: Request, request_body: SearchSchema):
    """ Search API to get the relevant results based on user query """
    log.set_logger("search", f"=== Inside search api ===", action="info")
    
    search_results = await crud.get_search_results(request_body)
    return search_results
    

