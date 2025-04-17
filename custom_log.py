import logging

def set_logger(logger_name, message, action="debug"):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    # Prevent multiple handlers
    if not logger.handlers:
        action_handler = logging.FileHandler('action.log', mode='a')  # append mode
        action_handler.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        action_handler.setFormatter(formatter)

        logger.addHandler(action_handler)

        # Optional: Prevent propagation to root logger (which prints to console)
        logger.propagate = False

    # Log the message
    if action == "debug":
        logger.debug(message)
    elif action == "info":
        logger.info(message)
    elif action == "error":
        logger.error(message, exc_info=True)
    else:
        logger.warning(f"Unknown log action: {action}, message: {message}")
