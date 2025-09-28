import pandas as pd
import sqlite3
from pathlib import Path
from pipeline.logger import get_logger

logger = get_logger(__name__)


# Load grocery_sales data from CSV to database
def load_csv_to_sqlite(csv_path, db_path, table_name="sales"):
    logger.info(f"Loading CSV {csv_path} into {db_path}: {table_name}")

    # Get data from CSV
    try:
        df = pd.read_csv(csv_path)
        logger.debug(f"CSV columns: {list(df.columns)}")

    except FileNotFoundError:
        logger.critical(f"CSV file not found: {csv_path}")
        raise

    except Exception as e:
        logger.error(f"Failed to read CSV: {e}")
        raise

    # Insert data into database
    try:
        with sqlite3.connect(db_path) as conn:
            df.to_sql(table_name, conn, if_exists="replace", index=False)

        logger.info(f"Inserted {len(df)} rows into {table_name}")

    except sqlite3.Error as e:
        logger.critical(f"SQLite error: {e}")
        raise


# Extract data from database for dataframe
def extract_from_sql(db_path, table_name="sales"):
    logger.info(f"Extracting from {db_path}: {table_name}")

    try:
        with sqlite3.connect(db_path) as conn:
            df = pd.read_sql(f"SELECT * FROM {table_name}", conn)

        logger.info(f"Extracted {len(df)} rows from SQL")

        return df
    except sqlite3.Error as e:
        logger.critical(f"SQLite error during extract: {e}")
        raise


# Merge grocery_sales data with extra data
def merge_with_parquet(store_df, parquet_path):
    logger.info(f"Merging with parquet file {parquet_path}")

    try:
        extra_df = pd.read_parquet(parquet_path, engine="pyarrow")
    except FileNotFoundError:
        logger.critical(f"Parquet file not found: {parquet_path}")
    except Exception as e:
        logger.error(f"Failed to read parquet: {e}")
        raise

    if "index" not in store_df.columns or "index" not in extra_df.columns:
        logger.critical("Merge failed: 'index' column missing in one of the datasets")
        raise KeyError("'index' column required for merge")

    # Merge store df and extra df together
    merged_df = store_df.merge(extra_df, on="index")

    missing = merged_df["index"].isna().sum()

    if missing > 0:
        logger.warning(f"{missing} rows had no match in Parquet file")

    logger.info(f"Merged dataset has {len(merged_df)} rows")

    return merged_df
