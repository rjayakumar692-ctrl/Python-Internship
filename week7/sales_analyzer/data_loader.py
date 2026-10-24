
from pathlib import Path
import pandas as pd


class SalesDataLoader:
    """Load sales data from CSV or Excel files."""

    REQUIRED_COLUMNS = [
        "order_id",
        "order_date",
        "customer_id",
        "product_id",
        "product_name",
        "category",
        "quantity",
        "unit_price",
        "total_amount",
        "region",
    ]

    def load_data(self, file_path):
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        extension = path.suffix.lower()

        if extension == ".csv":
            df = pd.read_csv(path)
        elif extension in (".xlsx", ".xls"):
            df = pd.read_excel(path)
        else:
            raise ValueError("Supported formats are CSV, XLSX and XLS.")

        df.columns = (
            df.columns.astype(str)
            .str.strip()
            .str.lower()
            .str.replace(r"[\s-]+", "_", regex=True)
        )

        if df.empty:
            raise ValueError("The sales data file is empty.")

        missing = [
            column for column in self.REQUIRED_COLUMNS
            if column not in df.columns
        ]

        if missing:
            raise ValueError(
                f"Missing required columns: {', '.join(missing)}"
            )

        return df

    @staticmethod
    def display_info(df):
        print("\n--- Sales Data Information ---")
        print(f"Rows: {len(df)}")
        print(f"Columns: {len(df.columns)}")
        print("\nColumn types:")
        print(df.dtypes)
        print("\nMissing values:")
        print(df.isna().sum())
        print("\nFirst five rows:")
        print(df.head())
