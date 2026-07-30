import logging
import sys
from logging.handlers import RotatingFileHandler
from src.taskflow.core.config import settings
import structlog
import logging

def setup_logging():
    root_logger = logging.getLogger()
    root_logger.setLevel(settings.LOG_LEVEL)

    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    formatter = logging.Formatter(settings.LOG_FORMAT)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    file_handler = RotatingFileHandler(
        "src.taskflow.log",
        maxBytes=5_000_000,
        backupCount=3,
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)

    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.add_log_level,
            structlog.processors.JSONRenderer()
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    logging.info("🚀 Logging system initialized successfully, bro!")


logger = structlog.get_logger()