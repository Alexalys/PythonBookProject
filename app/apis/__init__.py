import json
from fastapi import FastAPI
from app.apis.book_api import router as book_router
from app.utils.LoggerProvider import LoggerProvider
from app.db.database import engine, SessionLocal, Base

def load_config(file_path: str) -> dict:
    """
    Loads configuration from a JSON file.

    Args:
        file_path (str): Path to the configuration JSON file.

    Returns:
        dict: Loaded configuration as a dictionary.
    """
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file '{file_path}' not found.")
    except json.JSONDecodeError as e:
        raise ValueError(f"Error parsing JSON from '{file_path}': {str(e)}")

def configure_logging(log_file: str, log_level: str = "INFO") -> LoggerProvider:
    """
    Configures logging using LoggerProvider.

    Args:
        log_file (str): Path to the log file.
        log_level (str): Log level (default: "INFO").

    Returns:
        LoggerProvider: Configured logger provider instance.
    """
    return LoggerProvider(log_file=log_file, log_level=log_level)
    

# DB setup
Base.metadata.create_all(bind=engine)
# Application setup
project_prefix = "api/v1"
app = FastAPI()
logger_provider:LoggerProvider = configure_logging("app.log")
logger = logger_provider.get_logger()
# Load configuration
try:
    config = load_config("config/config.json")
    log_level:str = config.get("log_level", "INFO")
    logger_provider.set_level(log_level)
except (FileNotFoundError, ValueError) as e:
    logger.error(f"Failed to load configuration: {str(e)}")
    log_level = "INFO"

# Include routers
app.include_router(book_router)

