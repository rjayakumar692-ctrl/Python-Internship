
import pandas as pd


class SalesDataCleaner:
    """Clean and preprocess sales records."""

    REQUIRED_COLUMNS = [
        "order_id", "order_date", "customer_id", "product_id",
        "product_name", "category", "quantity", "unit_price",
        "total_amount", "region",
    ]

    TEXT_COLUMNS = [
        "customer_id", "product_id", "product_name", "category", "region"
    ]

    NUMERIC_COLUMNS = ["quantity", "unit_price", "total_amount"]

    def clean_data(self, df):
        data = df.copy()

        data.columns = (
            data.columns.astype(str)
            .str.strip()
            .str.lower()
            .str.replace(r"[\s-]+", "_", regex=True)
        )

        missing = [
            column for column in self.REQUIRED_COLUMNS
            if column not in data.columns
        ]
        if missing:
            raise ValueError(f"Missing columns: {missing}")

        data = data.drop_duplicates().copy()

        for column in self.TEXT_COLUMNS:
            data[column] = data[column].astype("string").str.strip()
            data[column] = data[column].replace("", pd.NA)

        data["order_date"] = pd.to_datetime(
            data["order_date"], errors="coerce"
        )

        for column in self.NUMERIC_COLUMNS:
            data[column] = pd.to_numeric(
                data[column], errors="coerce"
            )

        # A record without a valid date cannot be used for time analysis.
        data = data.dropna(subset=["order_date"]).copy()

        # Fill missing categorical values.
        for column in self.TEXT_COLUMNS:
            data[column] = data[column].fillna("Unknown")

        # Quantity and unit price are needed to calculate revenue.
        data = data.dropna(subset=["quantity", "unit_price"]).copy()
        data = data[
            (data["quantity"] > 0) & (data["unit_price"] >= 0)
        ].copy()

        # Calculate revenue consistently from quantity and price.
        data["total_amount"] = data["quantity"] * data["unit_price"]

        data["quantity"] = data["quantity"].astype(int)
        data["year"] = data["order_date"].dt.year
        data["month"] = data["order_date"].dt.month
        data["month_name"] = data["order_date"].dt.strftime("%B")
        data["month_year"] = data["order_date"].dt.to_period("M").astype(str)

        return data.reset_index(drop=True)

    @staticmethod
    def save_cleaned_data(df, file_path):
        from pathlib import Path

        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(path, index=False)
        print(f"Cleaned data saved to: {path}")
