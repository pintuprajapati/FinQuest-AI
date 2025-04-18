import logging_config
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from core.config import settings
from core import config
import os
import sys
from api.routes import router as api_router
from genai_stack.routes import router as genai_router
from langgraph_workflow.routes import router as langgraph_workflow_router
from utils import create_local_dir

SHOW_DOCS_ENVIRONMENT = ("local")  # explicit list of allowed envs

logger = logging.getLogger(__name__)

# set url for swagger docs as null if api is not public
openapi_url="/api/openapi.json" if settings.ENVIRONMENT in SHOW_DOCS_ENVIRONMENT else None

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        """Run initialization code once when app starts"""
        logger.info("\n**************** New log started ****************")
        
        # Create directories and log
        create_local_dir(settings.STATIC_DIR)
        create_local_dir(config.UPLOAD_DIR)
        create_local_dir(config.DOWNLOAD_DIR)
        create_local_dir(config.MD_FILES_DIR)
        create_local_dir(config.TEXT_FILES_DIR)
        yield
        logger.info(f"Lifespan exit - Clear the resources")
    except Exception as e:
        logger.error(f"Exceptoin in lifespan: {str(e)}")
    
# Initialize FastAPI app
app = FastAPI(
    lifespan=lifespan,
    title=settings.APP_NAME,
    debug=settings.DEBUG,
    openapi_url=openapi_url
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configure templates
templates = Jinja2Templates(directory="templates")

########################## Define Routers ########################## 
module_api_path = "/api/v1"
app.include_router(api_router, prefix=module_api_path)
app.include_router(genai_router, prefix=module_api_path)
app.include_router(langgraph_workflow_router, prefix=module_api_path)

########################## WEB UI (HTML) ##########################
# Home route 
@app.get("/", name="redirect-home")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


########################## Main ##########################
if __name__ == "__main__":
    try:
        import uvicorn
        logger.info("Starting Uvicorn server...")
        reload = True if (settings.ENVIRONMENT == "local") else False
        uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=reload)
    except KeyboardInterrupt:
        logger.info("Server shutting down...")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

