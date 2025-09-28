import pandas as pd
from pathlib import Path

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)


def make_csv():
    sales = pd.DataFrame(
        {
            "index": [0, 1, 2, 3, 4],
            "Store": [1, 1, 2, 2, 3],
            "Dept": [1, 2, 1, 2, 1],
            "Date": [
                "2023-01-05",
                "2023-02-10",
                "2023-03-15",
                "2023-04-20",
                "2023-05-25",
            ],
            "Weekly_Sales": [15000, 12000, 18000, 9000, 20000],
            "IsHoliday": [False, True, False, False, True],
            "Temperature": [42.3, 35.1, 60.2, 55.8, 70.5],
            "Fuel_Price": [3.59, 3.55, 3.61, 3.62, 3.65],
            "CPI": [220.3, None, 221.5, 222.2, None],
            "Unemployment": [7.8, 8.0, None, 7.3, 7.0],
            "MarkDown1": [100.0, None, 50.0, None, 80.0],
            "MarkDown2": [None, None, 30.0, None, 40.0],
            "MarkDown3": [50.0, None, None, None, 25.0],
            "MarkDown4": [None, 20.0, None, None, None],
            "MarkDown5": [None, None, 15.0, None, None],
            "Type": ["A", "B", "A", "C", "B"],
            "Size": [151315, 202307, 113501, 105000, 215000],
        }
    )

    sales.to_csv(DATA_DIR / "grocery_sales.csv", index=False)


def make_parquet():
    extra = pd.DataFrame(
        {
            "index": [0, 1, 2, 3],  # deliberately missing index 4
            "Category": ["Beverages", "Snacks", "Dairy", "Produce"],
            "Supplier": ["Supplier A", "Supplier B", "Supplier C", "Supplier D"],
        }
    )
    extra.to_parquet(DATA_DIR / "extra_data.parquet", engine="pyarrow", index=False)


if __name__ == "__main__":
    make_csv()
    make_parquet()
    print("✅ Sample data created in ./data/")
