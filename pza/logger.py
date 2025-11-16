from pza.prints import (
    print_error,
    print_footer,
    print_header,
    print_separator,
    print_subheader,
    print_with_label,
)

from logging.handlers import RotatingFileHandler
from logging import Logger
import logging
import sys

def get_logger(
    app_name: str,
    log_level: str = "info",
    log_file: str | None = None,
    max_bytes: int = 1_000_000,  # 1 MB per file
    backup_count: int = 5,       # keep 5 rotated files
) -> Logger:
    """
    Returns a configured logger for the given app.
    Logs to console and/or a rotating per-app log file.
    """
    if not app_name:
        print(f"Invalid app name")
        return None

    # Get or create logger
    app_logger = logging.getLogger(app_name)
    if app_logger.handlers:
        # Avoid double setup if called multiple times
        return app_logger

    # Set the logging level
    # Convert level string to logging constant (default to INFO)
    if not log_level:
        log_level = "info"
    log_level_constant = getattr(logging, log_level.upper(), logging.INFO)
    app_logger.setLevel(log_level_constant)

    # Set formatting options
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Handle console output
    if log_level.upper() == 'DEBUG':
        # Log to console if in DEBUG mode
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        app_logger.addHandler(console_handler)

    # Handle log files with rotation
    if log_file:
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding="utf-8",
        )
        file_handler.setFormatter(formatter)
        app_logger.addHandler(file_handler)

    return app_logger

if __name__ == "__main__":

    print_header(__file__)

    print_separator()

    print_subheader(f"Loading logger")

    print(get_logger("test_app"))
    print()

    print_footer()
