import os
import pandas as pd
from pandas.errors import EmptyDataError
from pipeline.logger import get_logger

logger = get_logger(__name__)


def validate(file_path):
    logger.info(f"Validating file: {file_path}")

    if not os.path.exists(file_path):
        logger.critical(f"Validation failed: {file_path} not found")
        raise FileNotFoundError(f"There is no file at path {file_path}")

    try:
        df = pd.read_csv(file_path)
    except EmptyDataError:
        logger.critical(f"Validation failed: {file_path} is empty")
        raise ValueError(f"Validation failed: {file_path} is empty")
    except Exception as e:
        logger.critical(f"Validation failed: Could not read {file_path} -> {e}")
        raise

    if df.empty:
        logger.critical(f"Validation failed: {file_path} is empty")
        raise ValueError(f"Validation failed: {file_path} is empty")

    logger.info(f"Validation passed: {file_path}")
    return True
