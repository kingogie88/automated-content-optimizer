import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
import json
from datetime import datetime

# Create logs directory
LOGS_DIR = Path("logs")
LOGS_DIR.mkdir(exist_ok=True)

# Configure logging format
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_LEVEL = logging.INFO

def setup_logger(name: str) -> logging.Logger:
    """Set up logger with file and console handlers."""
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)
    
    # Create formatters
    formatter = logging.Formatter(LOG_FORMAT)
    
    # File handler (rotating)
    file_handler = RotatingFileHandler(
        LOGS_DIR / f"{name}.log",
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    file_handler.setFormatter(formatter)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    
    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

class LoggedError(Exception):
    """Custom exception that ensures errors are logged."""
    def __init__(self, message: str, logger: logging.Logger):
        super().__init__(message)
        logger.error(message)

def log_function_call(logger: logging.Logger):
    """Decorator to log function calls with parameters and results."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Create log entry
            log_entry = {
                "function": func.__name__,
                "timestamp": datetime.now().isoformat(),
                "args": str(args),
                "kwargs": str(kwargs)
            }
            
            try:
                # Execute function
                result = func(*args, **kwargs)
                
                # Log success
                log_entry["status"] = "success"
                logger.info(f"Function call: {json.dumps(log_entry)}")
                
                return result
                
            except Exception as e:
                # Log error
                log_entry["status"] = "error"
                log_entry["error"] = str(e)
                logger.error(f"Function error: {json.dumps(log_entry)}")
                raise
                
        return wrapper
    return decorator 