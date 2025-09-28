import argparse
from pathlib import Path
from pipeline.extract import load_csv_to_sqlite, extract_from_sql, merge_with_parquet
from pipeline.extract import load_csv_to_sqlite, extract_from_sql, merge_with_parquet
from pipeline.transform import transform, avg_weekly_sales_per_month
from pipeline.load import load
from pipeline.validate import validate
from pipeline.logger import get_logger

logger = get_logger("pipeline")

DATA_DIR = Path("data")
LOG_DIR = Path("logs")
CSV_PATH = DATA_DIR / "grocery_sales.csv"
DB_PATH = DATA_DIR / "grocery.db"
PARQUET_PATH = DATA_DIR / "extra_data.parquet"


def run_pipeline(dry_run=False):

    logger.info("Pipeline started")

    try:
        # Extract
        load_csv_to_sqlite(CSV_PATH, DB_PATH)
        sql_df = extract_from_sql(DB_PATH)
        merged_df = merge_with_parquet(sql_df, PARQUET_PATH)

        # Transform
        clean_df = transform(merged_df)
        agg_df = avg_weekly_sales_per_month(clean_df)

        logger.info(
            f"Pipeline summary: {len(sql_df)} input rows -> {len(clean_df)} cleaned rows -> {len(agg_df)} aggregated rows"
        )

        if not dry_run:
            DATA_DIR.mkdir(exist_ok=True)
            clean_path = DATA_DIR / "clean_data.csv"
            agg_path = DATA_DIR / "agg_data.csv"
            clean_df.to_csv(clean_path, index=False)
            agg_df.to_csv(agg_path, index=False)

            validate(clean_path)
            validate(agg_path)

        logger.info("Pipeline finished successfully")

    except Exception as e:
        logger.critical(f"Pipeline failed: {e}", exc_info=True)
        raise


# This will check if the run docker command was a dry run or not
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run grocery ETL pipeline")
    parser.add_argument(
        "--dry-run", action="store_true", help="Run pipeline without writing files"
    )
    args = parser.parse_args()

    run_pipeline(dry_run=args.dry_run)
