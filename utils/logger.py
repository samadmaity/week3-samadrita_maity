from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LOG_FILE = PROJECT_ROOT / "app.log"

APP_LOGGER_NAME = "shopping_api"
DEFAULT_LOG_LEVEL = logging.INFO

LOG_FORMAT = (
    "%(asctime)s - %(levelname)s - "
    "%(name)s - %(message)s"
)
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

MAX_LOG_SIZE = 5 * 1024 * 1024
BACKUP_COUNT = 3
HANDLER_MARKER = "_shopping_api_handler"


def configure_logging(
    log_file: str | Path = DEFAULT_LOG_FILE,
    level: int = DEFAULT_LOG_LEVEL,
) -> logging.Logger:
    """Configure console and rotating file logging."""

    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    application_logger = logging.getLogger(APP_LOGGER_NAME)
    application_logger.setLevel(level)
    application_logger.propagate = False

    for handler in application_logger.handlers[:]:
        if getattr(handler, HANDLER_MARKER, False):
            application_logger.removeHandler(handler)
            handler.close()

    formatter = logging.Formatter(
        fmt=LOG_FORMAT,
        datefmt=DATE_FORMAT,
    )

    file_handler = RotatingFileHandler(
        filename=log_path,
        maxBytes=MAX_LOG_SIZE,
        backupCount=BACKUP_COUNT,
        encoding="utf-8",
    )
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    setattr(file_handler, HANDLER_MARKER, True)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    setattr(console_handler, HANDLER_MARKER, True)

    application_logger.addHandler(file_handler)
    application_logger.addHandler(console_handler)

    return application_logger


logger = configure_logging()

logger.info("Shopping API logging initialized")


if __name__ == "__main__":
    logger.info("Logger test message: logging is working.")
    print(f"Log file created at: {DEFAULT_LOG_FILE}")

