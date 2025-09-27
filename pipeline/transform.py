import pandas as pd
from pipeline.logger import get_logger

logger = get_logger(__name__)


def transform(raw_data):
    logger.info("Starting transform step")

    # Check how many NaNs exist
    missing_counts = {
        col: raw_data[col].isna().sum()
        for col in ["CPI", "Weekly_Sales", "Unemployment"]
        if col in raw_data.columns
    }

    # Fill missing numeric values
    raw_data.fillna(
        {
            "CPI": raw_data["CPI"].mean(),
            "Weekly_Sales": raw_data["Weekly_Sales"].mean(),
            "Unemployment": raw_data["Unemployment"].mean(),
        },
        inplace=True,
    )

    for col, count in missing_counts.items():
        if count > 0:
            logger.warning(f"Filled {count} missing values in '{col}' with mean")

    # Convert Date and extract Month
    raw_data["Date"] = pd.to_datetime(raw_data["Date"], format="%Y-%m-%d")
    raw_data["Month"] = raw_data["Date"].dt.month

    # Filter for high weekly sales
    before = len(raw_data)

    raw_data = raw_data.loc[raw_data["Weekly_Sales"] > 10000, :]

    logger.info(f"Filtered {before - len(raw_data)} rows with low sales")

    # Drop unused columns
    drop_cols = [
        "index",
        "Temperature",
        "Fuel_Price",
        "MarkDown1",
        "MarkDown2",
        "MarkDown3",
        "MarkDown4",
        "MarkDown5",
        "Type",
        "Size",
        "Date",
    ]

    # Check if columns to drop exist
    existing = [c for c in drop_cols if c in raw_data.columns]

    raw_data = raw_data.drop(existing, axis=1)

    logger.info("Transform step complete")

    return raw_data


def avg_weekly_sales_per_month(clean_data):
    logger.info("Aggregating average weekly sales per month")

    try:
        holiday_sales = (
            clean_data.groupby("Month")["Weekly_Sales"]
            .mean()
            .reset_index(name="Avg_Sales")
            .round(2)
        )

        logger.info("Aggregation complete")
        return holiday_sales
    except KeyError as e:
        logger.critical(f"Aggregation failed: missing column: {e}")
        raise
