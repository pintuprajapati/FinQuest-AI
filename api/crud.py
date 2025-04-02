from utils import create_response
import custom_log as log

async def get_search_results(request_body):
    """ Search the results based on user query """
    try:
        log.set_logger("get_search_results", f"Getting search results based on user query...", action="info")
        user_query = request_body.user_query
        # Some code
        result_data = {}
        log.set_logger("get_search_results", f"Results are fetched successfully", action="info")
        return create_response(message="Results are fetched successfully", status_code=200, success=True, data=result_data)
    except Exception as e:
        log.set_logger("get_search_results", f"exception: {str(e)}", action="error")
        return create_response(message=str(e), status_code=500, success=False, data={})
    