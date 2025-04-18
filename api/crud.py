from utils import create_response
import logging
logger = logging.getLogger(__name__)

async def get_search_results(request_body):
    """ Search the results based on user query """
    try:
        logger.info(f"Getting search results based on user query...")
        user_query = request_body.user_query
        # Some code
        result_data = {}
        logger.info(f"Results are fetched successfully")
        return create_response(message="Results are fetched successfully", status_code=200, success=True, data=result_data)
    except Exception as e:
        logger.error(f"exception: {str(e)}")
        return create_response(message=str(e), status_code=500, success=False, data={})
    