import pandas as pd
from pipeline.transform import transform


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
