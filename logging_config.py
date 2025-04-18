import logging
from pathlib import Path

# Create logs directory first
logs_dir = Path("logs")
logs_dir.mkdir(exist_ok=True)

# Configure root logger instead of module-specific logger
logging.basicConfig(
    level=logging.DEBUG,  # Root logger set to DEBUG
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/project.log"),  # File handler shows INFO+ 
        logging.StreamHandler()  # Console shows INFO+
    ]
)

# Add suppression for common noisy loggers
loggers_to_suppress = [
    'httpcore', 'httpx', 'openai', 
    'chromadb', 'httpcore.connection',
    'httpcore.http11', 'urllib3'
]

for logger_name in loggers_to_suppress:
    logging.getLogger(logger_name).setLevel(logging.WARNING)

# Add this line to suppress watchfiles INFO messages
logging.getLogger('watchfiles.main').setLevel(logging.WARNING)
