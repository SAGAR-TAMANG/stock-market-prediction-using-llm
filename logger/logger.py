import logging
import colorlog

def setup_logger(name="my_logger"):
    logger = logging.getLogger(name)

    # Avoid duplicate handlers
    if not logger.hasHandlers():
        # Create colored formatter
        formatter = colorlog.ColoredFormatter(
            "%(log_color)s%(levelname)-8s %(message)s%(reset)s",
            log_colors={
                "DEBUG": "cyan",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "bold_red",
            },
        )

        # Console handler
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)

        # Add handler to logger
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)

    return logger

# Example Usage
logger = setup_logger()
logger.debug("This is a debug message.")
logger.info("This is an info message.")
logger.warning("This is a warning message.")
logger.error("This is an error message.")
logger.critical("This is a critical message.")
