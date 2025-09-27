import pandas as pd
from pathlib import Path
from pipeline.logger import get_logger

logger = get_logger(__name__)


def load(clean_df, clean_path, agg_df, agg_path):
    try:
        clean_df.to_csv(clean_path, index=False)
        logger.info(f"Saved cleaned data to {clean_path}")

        agg_df.to_csv(agg_path, index=False)
        logger.info(f"Saved aggregated data to {agg_path}")

    except Exception as e:
        logger.critical(f"Failed to save CSV files: {e}")
        raise

    logger.info("Load step completed")
