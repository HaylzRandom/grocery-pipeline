import logging
from pathlib import Path
from colorama import Fore, Style, init

# Check logs directory exists
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "pipeline.log"


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:  # Prevent duplicate handlers
        logger.propagate = False

        # Make log messages colourful and distinctful
        def add_colour(record, msg):
            if record.levelno == logging.INFO:
                return f"{Fore.GREEN}{msg}{Style.RESET_ALL}"
            elif record.levelno == logging.WARNING:
                return f"{Fore.YELLOW}{msg}{Style.RESET_ALL}"
            elif record.levelno == logging.ERROR:
                return f"{Fore.RED}{msg}{Style.RESET_ALL}"
            if record.levelno == logging.CRITICAL:
                return f"{Style.BRIGHT}{Fore.RED}{msg}{Style.RESET_ALL}"

            return msg

        class ColourFormatter(logging.Formatter):
            def format(self, record):
                msg = super().format(record)
                return add_colour(record, msg)

        # Console Handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        console_handler.setFormatter(
            ColourFormatter(
                "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
        )

        # File Handler
        file_handler = logging.FileHandler(LOG_FILE)
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        file_handler.setFormatter(file_formatter)

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger
