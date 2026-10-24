
import argparse
from pathlib import Path

from sales_analyzer import (
    SalesDataLoader,
    SalesDataCleaner,
    SalesAnalyzer,
    SalesVisualizer,
    SalesReporter,
)


BASE_DIR = Path(__file__).resolve().parent
DEFAULT_DATA = BASE_DIR / "data" / "raw" / "sales_data.csv"
PROCESSED_DATA = BASE_DIR / "data" / "processed" / "sales_data_cleaned.csv"


def main():
    parser = argparse.ArgumentParser(
        description="Sales Data Analysis Dashboard"
    )
    parser.add_argument(
        "--file",
        default=str(DEFAULT_DATA),
        help="Path to the sales CSV or Excel file",
    )
    parser.add_argument(
        "--action",
        choices=[
            "info", "stats", "categories", "products", "monthly",
            "customers", "regions", "forecast", "visualize",
            "report", "all",
        ],
        default="all",
        help="Analysis to run",
    )
    args = parser.parse_args()

    loader = SalesDataLoader()
    cleaner = SalesDataCleaner()

    raw_df = loader.load_data(args.file)
    loader.display_info(raw_df)

    df = cleaner.clean_data(raw_df)
    cleaner.save_cleaned_data(df, PROCESSED_DATA)

    print(f"\nRaw rows: {len(raw_df)}")
    print(f"Cleaned rows: {len(df)}")

    analyzer = SalesAnalyzer(df)
    action = args.action

    if action in ("info", "all"):
        print("\n--- Cleaned Data Preview ---")
        print(df.head())

    if action in ("stats", "all"):
        print("\n--- Basic Statistics ---")
        for key, value in analyzer.calculate_basic_stats().items():
            print(f"{key.replace('_', ' ').title()}: {value}")

    if action in ("categories", "all"):
        print("\n--- Sales by Category ---")
        print(analyzer.sales_by_category().to_string(index=False))

    if action in ("products", "all"):
        print("\n--- Top 5 Products ---")
        print(analyzer.top_products(5).to_string(index=False))

    if action in ("monthly", "all"):
        print("\n--- Monthly Sales ---")
        print(analyzer.monthly_sales().to_string(index=False))

    if action in ("customers", "all"):
        print("\n--- Top 10 Customers ---")
        print(analyzer.customer_analysis().head(10).to_string(index=False))

    if action in ("regions", "all"):
        print("\n--- Sales by Region ---")
        print(analyzer.sales_by_region().to_string(index=False))

    if action in ("forecast", "all"):
        print("\n--- Monthly Sales Forecast ---")
        print(analyzer.monthly_sales_forecast().to_string(index=False))

    if action in ("visualize", "all"):
        visualizer = SalesVisualizer(BASE_DIR / "output")
        visualizer.generate_all(analyzer)

    if action in ("report", "all"):
        reporter = SalesReporter(BASE_DIR / "data" / "reports")
        reporter.generate_all(analyzer)

    print("\nAnalysis completed successfully.")


if __name__ == "__main__":
    main()
