import os
from pipeline.logger import get_logger

logger = get_logger(__name__)


def validate(file_path):
    logger.info(f"Validating file: {file_path}")

    if not os.path.exists(file_path):
        logger.critical(f"Validation failed: {file_path} not found")
        raise FileNotFoundError(f"There is no file at path {file_path}")

    logger.info(f"Validation passed: {file_path}")
