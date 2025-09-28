import pytest
from pipeline.main import run_pipeline
from pipeline import main
import logging
import pandas as pd


@pytest.mark.integration
def test_pipeline_dry_run(tmp_path, caplog):
    # Capture logs from pipeline loggers
    logging.getLogger("pipeline").propagate = True
    logging.getLogger("pipeline.main").propagate = True
    logging.getLogger("pipeline.extract").propagate = True
    logging.getLogger("pipeline.transform").propagate = True
    caplog.set_level("INFO")

    # Redirect pipeline paths to temporary directory
    main.DATA_DIR = tmp_path
    main.CSV_PATH = tmp_path / "grocery_sales.csv"
    main.DB_PATH = tmp_path / "grocery.db"
    main.PARQUET_PATH = tmp_path / "extra_data.parquet"

    # Create fake data
    sales = pd.DataFrame(
        {
            "index": [0, 1],
            "Date": ["2023-01-01", "2023-02-01"],
            "Weekly_Sales": [15000, 20000],
            "CPI": [220.5, 221.1],
            "Unemployment": [7.5, 7.3],
        }
    )

    sales.to_csv(main.CSV_PATH, index=False)

    extra = pd.DataFrame(
        {
            "index": [0, 1],
            "Category": ["Snacks", "Dairy"],
            "Supplier": ["Supplier A", "Supplier B"],
        }
    )

    extra.to_parquet(main.PARQUET_PATH, engine="pyarrow", index=False)

    # Run pipeline (dry run, so no CSV writes)
    run_pipeline(dry_run=True)

    print(caplog.text)

    assert "Pipeline summary:" in caplog.text
    assert "Extracted" in caplog.text
    assert "Transform step complete" in caplog.text
    assert "Pipeline finished successfully" in caplog.text
