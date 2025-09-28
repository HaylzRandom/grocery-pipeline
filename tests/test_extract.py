import pandas as pd
from pathlib import Path
from pipeline.extract import load_csv_to_sqlite, extract_from_sql, merge_with_parquet


def test_load_and_extract(tmp_path):
    csv_path = tmp_path / "sales.csv"
    db_path = tmp_path / "test.db"
    df = pd.DataFrame({"Date": ["2023-01-01"], "Weekly_Sales": [15000]})
    df.to_csv(csv_path, index=False)

    load_csv_to_sqlite(csv_path, db_path, table_name="sales")
    out = extract_from_sql(db_path, table_name="sales")

    assert len(out) == 1
    assert out.iloc[0]["Weekly_Sales"] == 15000


def test_merge_with_parquet(tmp_path):
    base_df = pd.DataFrame(
        {"index": [0], "Date": ["2023-01-01"], "Weekly_Sales": [15000]}
    )
    parquet_path = tmp_path / "extra.parquet"
    pd.DataFrame({"index": [0], "Category": ["Snacks"]}).to_parquet(
        parquet_path, engine="pyarrow", index=False
    )

    merged = merge_with_parquet(base_df, parquet_path)

    assert "Category" in merged.columns
    assert merged.iloc[0]["Category"] == "Snacks"
