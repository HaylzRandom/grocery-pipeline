import pandas as pd
from pipeline.transform import transform, avg_weekly_sales_per_month


def test_transform_filters_and_fill():
    df = pd.DataFrame(
        {
            "Date": ["2023-01-01", "2023-01-02"],
            "Weekly_Sales": [15000, None],  # one above threshold, one missing
            "CPI": [None, 220.0],  # one missing CPI
            "Unemployment": [7.5, None],  # one missing Unemployment
        }
    )

    result = transform(df)

    # Expect at least 1 row left after filtering
    assert len(result) >= 1

    # CPI, Unemployment and Weekly_Sales should have no NaNs
    assert result["CPI"].isna().sum() == 0
    assert result["Unemployment"].isna().sum() == 0
    assert result["Weekly_Sales"].isna().sum() == 0


def test_avg_weekly_sales_per_month():
    df = pd.DataFrame(
        {
            "Date": pd.to_datetime(["2023-01-01", "2023-01-15", "2023-02-01"]),
            "Weekly_Sales": [10000, 20000, 30000],
        }
    )

    # Simulate transform step extracting Month from Date
    df["Month"] = df["Date"].dt.month

    agg = avg_weekly_sales_per_month(df)

    assert len(agg) == 2
    assert "Month" in agg.columns
    assert "Avg_Sales" in agg.columns
    assert set(agg["Month"]) == {1, 2}
    assert agg.loc[agg["Month"] == 1, "Avg_Sales"].iloc[0] == 15000
