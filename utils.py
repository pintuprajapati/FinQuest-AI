from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from core.config import settings
import os
import shutil
import custom_log as log
import aiohttp
from urllib.parse import urlparse
from pathlib import Path
import uuid

# General JSON response to return in API response
def create_response(message: str, status_code: int, success: bool = False, **kwargs):
    """ General JSON response """
    
    return JSONResponse(
      status_code = status_code,
      content = {
          'success': success,
          'message': message,
          **jsonable_encoder(kwargs)
        }
    )

def create_local_dir(path):
  try:
    # Create upload directory if it doesn't exist
    os.makedirs(path, exist_ok=True)
  except Exception as e:
    log.set_logger("create_local_dir", f"Exception: {str(e)}", action="error")
    
def delete_local_file_dir(path):
  try:
    # Check if path exists
    if not os.path.exists(path):
      print(f"Path '{path}' doesn't exist")
      log.set_logger("delete_local_dir", f"Path '{path}' doesn't exist", action="info")
      return False
    
    # Delete file or directory
    if os.path.isfile(path):
      os.remove(path)
      log.set_logger("delete_local_dir", f"File '{path}' deleted successfully", action="info")
    else:
      shutil.rmtree(path)
      log.set_logger("delete_local_dir", f"Directory '{path}' deleted successfully", action="info")
    return True
  except Exception as e:
    log.set_logger("delete_local_dir", f"Exception: {str(e)}", action="error")
    return False
  
async def download_file_to_local(url: str, local_dir: str, filename: str = None) -> str:
  """
  Downloads a file from a URL to a local directory asynchronously.
  
  Args:
      url: The URL of the file to download (can be S3 or any web URL)
      local_dir: The directory where the file should be saved
      filename: Optional custom filename. If not provided, extracts from URL
  
  Returns:
      The full path to the downloaded file or None if download fails
  """
  try:
    # Create directory if it doesn't exist
    create_local_dir(local_dir)
    
    # If filename not provided, extract from URL
    if not filename:
      parsed_url = urlparse(url)
      filename = os.path.basename(parsed_url.path)
      # If no filename in URL, use a default
      if not filename:
        filename = f"downloaded_file_{str(uuid.uuid4())}"
    
    # Full path where the file will be saved
    file_path = os.path.join(local_dir, filename)
    
    # Download the file asynchronously
    log.set_logger("download_file_to_local", f"Starting download from {url}", action="info")
    
    async with aiohttp.ClientSession() as session:
      async with session.get(url) as response:
        if response.status != 200:
          log.set_logger("download_file_to_local", f"Failed to download file: HTTP {response.status}", action="error")
          return None
        
        # Save file to disk
        with open(file_path, 'wb') as f:
          while True:
            chunk = await response.content.read(1024)
            if not chunk:
              break
            f.write(chunk)
    
    log.set_logger("download_file_to_local", f"File downloaded successfully to {file_path}", action="info")
    return file_path
  
  except Exception as e:
    log.set_logger("download_file_to_local", f"Exception: {str(e)}", action="error")
    return None 