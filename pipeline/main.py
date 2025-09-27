from pathlib import Path
from pipeline.extract import load_csv_to_sqlite, extract_from_sql, merge_with_parquet
from pipeline.extract import load_csv_to_sqlite, extract_from_sql, merge_with_parquet
from pipeline.transform import transform, avg_weekly_sales_per_month
from pipeline.load import load
from pipeline.validate import validate
from pipeline.logger import get_logger

logger = get_logger("pipeline")

DB_PATH = Path("data/grocery_sales.db")
CSV_PATH = Path("data/grocery_sales.csv")
SQL_TABLE = "grocery_sales"
PARQUET_PATH = Path("data/extra_data.parquet")
CLEAN_PATH = Path("data/clean_data.csv")
AGG_PATH = Path("data/agg_data.csv")

if __name__ == "__main__":
    logger.info("Pipeline started")

    try:
        # Extract
        load_csv_to_sqlite(CSV_PATH, DB_PATH, SQL_TABLE)
        sql_df = extract_from_sql(DB_PATH, SQL_TABLE)
        merged_df = merge_with_parquet(sql_df, PARQUET_PATH)

        # Transform
        clean_df = transform(merged_df)
        agg_df = avg_weekly_sales_per_month(clean_df)

        # Load
        load(clean_df, CLEAN_PATH, agg_df, AGG_PATH)
        validate(CLEAN_PATH)
        validate(AGG_PATH)

        logger.info(
            f"Pipeline summary: {len(sql_df)} -> {len(clean_df)} -> {len(agg_df)}"
        )
        logger.info("Pipeline finished successfully")

    except Exception as e:
        logger.critical(f"Pipeline failed: {e}")
        raise
