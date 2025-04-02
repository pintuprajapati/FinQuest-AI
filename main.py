from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from core.config import settings
import os
import sys
from api.routes import router as api_router
from genai_stack.routes import router as genai_router
import custom_log as log
from utils import create_local_dir

SHOW_DOCS_ENVIRONMENT = ("local")  # explicit list of allowed envs

# set url for swagger docs as null if api is not public
openapi_url="/api/openapi.json" if settings.ENVIRONMENT in SHOW_DOCS_ENVIRONMENT else None

log.set_logger("main", f"\n**************** New log started ****************", action="info")

create_local_dir(settings.STATIC_DIR)

# Initialize FastAPI app
app = FastAPI(
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

########################## WEB UI (HTML) ##########################
# Home route 
@app.get("/", name="redirect-home")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


########################## Main ##########################
if __name__ == "__main__":
    try:
        import uvicorn
        # if env is "local" then reload the server on every change
        reload = True if (settings.ENVIRONMENT == "local") else False
        uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=reload)
    except KeyboardInterrupt:
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

