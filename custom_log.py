import logging

# Function to set up logger and log messages
def set_logger(logger_name, message, action="debug"):
    # Get the logger by name or create a new one
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    
    # Check if the logger already has handlers (to avoid duplicates)
    if not logger.hasHandlers():
        # Create handlers for status.log and action.log
        # status_handler = logging.FileHandler('status.log')
        # status_handler.setLevel(logging.INFO)  # Captures INFO and ERROR

        action_handler = logging.FileHandler('action.log')
        action_handler.setLevel(logging.DEBUG)  # Captures DEBUG, INFO, and ERROR

        # Create formatters and add them to the handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        # status_handler.setFormatter(formatter)
        action_handler.setFormatter(formatter)

        # Add the handlers to the logger
        # logger.addHandler(status_handler)
        logger.addHandler(action_handler)
    
    # Log the message based on the action
    if action == "debug":
        logger.debug(message)  # This will only go to action.log
    elif action == "info":
        logger.info(message)  # This will go to both status.log and action.log
    elif action == "error":
        logger.error(message,exc_info=True)  # This will go to both status.log and action.log
    else:
        logger.warning(f"Unknown log action: {action}, message: {message}")

# Example usage
# set_logger("create_graph", "This is a debug message", action="debug") 
# set_logger("create_doc", "This is an info message", action="info")    
# set_logger("create_doc", "This is an error message", action="error")   # Goes to both status.log and action.log
