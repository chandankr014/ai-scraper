"""
Centralized logging configuration for Flood Intelligence API.
"""
import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from datetime import datetime

# Log directory
LOG_DIR = Path(__file__).parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

# Log format with full details
FILE_FORMAT = (
    "%(asctime)s | %(levelname)-8s | %(name)s | "
    "%(funcName)s:%(lineno)d | %(message)s"
)
CONSOLE_FORMAT = "%(asctime)s | %(levelname)-8s | %(message)s"

# Module-level logger cache
_loggers = {}


def setup_logging(
    name: str = "flood_intel",
    level: str = "DEBUG",
    log_file: str = None
) -> logging.Logger:
    """
    Configure comprehensive logging system.
    
    Features:
    - Rotating file handler (10MB max, 5 backups)
    - Console output with cleaner format
    - Full trace in file logs
    - Separate error log for quick debugging
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper(), logging.DEBUG))
    logger.handlers.clear()
    
    # Timestamp for log file
    timestamp = datetime.now().strftime("%Y%m%d")
    log_file = log_file or f"flood_intel_{timestamp}.log"
    
    # File handler - detailed logging
    file_handler = RotatingFileHandler(
        LOG_DIR / log_file,
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5,
        encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(FILE_FORMAT, datefmt="%Y-%m-%d %H:%M:%S"))
    
    # Error file handler - errors only
    error_handler = RotatingFileHandler(
        LOG_DIR / f"flood_intel_errors_{timestamp}.log",
        maxBytes=5 * 1024 * 1024,
        backupCount=3,
        encoding="utf-8"
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(logging.Formatter(FILE_FORMAT, datefmt="%Y-%m-%d %H:%M:%S"))
    
    # Console handler - cleaner output
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter(CONSOLE_FORMAT, datefmt="%H:%M:%S"))
    
    logger.addHandler(file_handler)
    logger.addHandler(error_handler)
    logger.addHandler(console_handler)
    
    # Silence noisy libraries
    for lib in ['urllib3', 'httpx', 'httpcore', 'asyncio', 'playwright']:
        logging.getLogger(lib).setLevel(logging.WARNING)
    
    logger.info(f"Logging initialized: level={level}, file={log_file}")
    return logger


# Track if logging has been initialized
_initialized = False


def get_logger(name: str) -> logging.Logger:
    """Get a child logger for a specific module."""
    global _initialized
    if not _initialized:
        setup_logging()
        _initialized = True
    if name not in _loggers:
        _loggers[name] = logging.getLogger(f"flood_intel.{name}")
    return _loggers[name]
