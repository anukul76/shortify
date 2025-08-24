import logging
import logging.config
from typing import Dict, Any


def get_logging_config() -> Dict[str, Any]:
    """
    Returns the logging configuration dictionary
    """
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S"
            },
            "detailed": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S"
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": "INFO",
                "formatter": "default",
                "stream": "ext://sys.stdout"
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "DEBUG",
                "formatter": "detailed",
                "filename": "logs/app.log",
                "maxBytes": 10485760,  # 10MB
                "backupCount": 5,
                "encoding": "utf8"
            },
            "error_file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "ERROR",
                "formatter": "detailed",
                "filename": "logs/error.log",
                "maxBytes": 10485760,  # 10MB
                "backupCount": 5,
                "encoding": "utf8"
            }
        },
        "loggers": {
            "": {  # root logger
                "level": "INFO",
                "handlers": ["console", "file", "error_file"]
            },
            "app.payments": {
                "level": "DEBUG",
                "handlers": ["console", "file", "error_file"],
                "propagate": False
            },
            "requests": {
                "level": "WARNING",
                "propagate": True
            },
            "urllib3": {
                "level": "WARNING", 
                "propagate": True
            }
        }
    }


def setup_logging(log_level: str = "INFO"):
    """
    Setup logging configuration
    
    Args:
        log_level: The minimum log level to use (DEBUG, INFO, WARNING, ERROR)
    """
    import os
    from pathlib import Path
    
    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Get the configuration and optionally override log level
    config = get_logging_config()
    
    # Override log level if specified
    if log_level.upper() in ["DEBUG", "INFO", "WARNING", "ERROR"]:
        config["loggers"][""]["level"] = log_level.upper()
        config["handlers"]["console"]["level"] = log_level.upper()
    
    # Apply logging configuration
    try:
        logging.config.dictConfig(config)
        print(f"Logging configured successfully with level: {log_level}")
    except Exception as e:
        print(f"Failed to configure logging: {e}")
        # Fallback to basic logging
        logging.basicConfig(
            level=getattr(logging, log_level.upper(), logging.INFO),
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance with the given name
    
    Args:
        name: The name of the logger (usually __name__)
        
    Returns:
        Logger instance
    """
    return logging.getLogger(name)
