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
import datetime
import random
import utils
import json
import re

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
    return e
  
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
        filename = utils.add_timestamp_to_filename("downloaded_file")
      else:
        filename = utils.add_timestamp_to_filename(filename)
    
    # Full path where the file will be saved
    file_path = os.path.join(local_dir, filename)
    
    # Download the file asynchronously
    log.set_logger("download_file_to_local", f"Starting download from '{url}'", action="info")
    
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
    
    log.set_logger("download_file_to_local", f"File downloaded successfully to '{file_path}'", action="info")
    return file_path
  
  except Exception as e:
    log.set_logger("download_file_to_local", f"Exception: {str(e)}", action="error")
    raise e
  
def add_timestamp_to_filename(filename):
    """
    add the 'timestamp_randomDigits' between filename and extension
    ex: filename.pdf => filename_123123_232423.pdf
    """
    
    # Get the current Unix timestamp in milliseconds
    timestamp = int(datetime.datetime.now().timestamp() * 1000) # ex: timestamp: 1740130919783
    
    # Generate five random digits
    random_digits = random.randint(10000, 999999)
    
    # Split filename and extension
    name, ext = filename.rsplit('.', 1)  # Splits only at the last '.'
    
    # Return new filename with timestamp and random number
    return f"{name}_{timestamp}_{random_digits}.{ext}"

def parse_llm_response(llm_response: str) -> dict:
  """ Convert LLM response (str type) into Dict type """
  try:
    if isinstance(llm_response, str):
            
      # Remove any surrounding code block markers or leading labels
      llm_response = llm_response.strip()
      
      # Remove triple backticks and language hints (e.g., ```json)
      llm_response = re.sub(r"```(?:json)?", "", llm_response).strip()

      match = re.search(r'\{.*\}', llm_response, re.DOTALL)
      if match:
          llm_response = match.group(0)

      try:
        return json.loads(llm_response)
      except json.JSONDecodeError as e:
        # Attempt to fix Python dict style (single quotes) to JSON
        try:
          safe_json = llm_response.replace("'", '"')
          return json.loads(safe_json)
        except Exception as inner_e:
          log.set_logger("extract_json", f"❌ Still failed to parse JSON: {inner_e}", action="debug")
          return {}
    else:
      log.set_logger("extract_json", f"⚠️ Unexpected llm_response type: {type(llm_response)}", action="debug")
      return None

  except Exception as e:
    log.set_logger("extract_json", f"Exception: {str(e)}", action="error")
    return e
