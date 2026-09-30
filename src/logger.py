import logging

from config import AppConfig


def setup_logger(config: AppConfig) -> logging.Logger:
    """Create and configure the application logger."""

    config.logs_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    log_file = config.logs_dir / config.log_file_name

    logger = logging.getLogger("invoice_automation")
    logger.setLevel(logging.INFO)

    # Prevent duplicate log messages if setup_logger() is called again.
    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Write logs to a file.
    file_handler = logging.FileHandler(
        log_file,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    # Also show logs in the terminal.
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger