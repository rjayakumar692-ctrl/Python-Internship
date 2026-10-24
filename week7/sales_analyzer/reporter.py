
from pathlib import Path
import pandas as pd


class SalesReporter:
    """Export analysis results and executive summaries."""

    def __init__(self, reports_dir="data/reports"):
        self.reports_dir = Path(reports_dir)
        self.reports_dir.mkdir(parents=True, exist_ok=True)

    def export_excel(self, analyzer):
        path = self.reports_dir / "sales_analysis_report.xlsx"

        with pd.ExcelWriter(path, engine="openpyxl") as writer:
            pd.DataFrame(
                list(analyzer.calculate_basic_stats().items()),
                columns=["Metric", "Value"],
            ).to_excel(writer, sheet_name="Summary", index=False)

            analyzer.sales_by_category().to_excel(
                writer, sheet_name="Categories", index=False
            )
            analyzer.top_products(10).to_excel(
                writer, sheet_name="Top Products", index=False
            )
            analyzer.monthly_sales().to_excel(
                writer, sheet_name="Monthly Sales", index=False
            )
            analyzer.sales_by_region().to_excel(
                writer, sheet_name="Regions", index=False
            )
            analyzer.customer_analysis().to_excel(
                writer, sheet_name="Customers", index=False
            )
            analyzer.monthly_sales_forecast().to_excel(
                writer, sheet_name="Forecast", index=False
            )

        print(f"Excel report saved: {path}")
        return path

    def export_csv_reports(self, analyzer):
        reports = {
            "category_sales.csv": analyzer.sales_by_category(),
            "top_products.csv": analyzer.top_products(10),
            "monthly_sales.csv": analyzer.monthly_sales(),
            "regional_sales.csv": analyzer.sales_by_region(),
            "customer_analysis.csv": analyzer.customer_analysis(),
            "sales_forecast.csv": analyzer.monthly_sales_forecast(),
        }

        paths = []
        for filename, df in reports.items():
            path = self.reports_dir / filename
            df.to_csv(path, index=False)
            paths.append(path)
            print(f"CSV report saved: {path}")

        return paths

    def export_executive_summary(self, analyzer):
        path = self.reports_dir / "executive_summary.txt"
        stats = analyzer.calculate_basic_stats()
        insights = analyzer.generate_insights()

        lines = [
            "SALES DATA ANALYSIS - EXECUTIVE SUMMARY",
            "=" * 45,
            "",
            f"Total records: {stats['total_records']}",
            f"Total revenue: {stats['total_revenue']:.2f}",
            f"Unique orders: {stats['total_orders']}",
            f"Unique customers: {stats['unique_customers']}",
            f"Unique products: {stats['unique_products']}",
            f"Units sold: {stats['total_units_sold']}",
            f"Average order value: {stats['average_order_value']:.2f}",
            "",
            "KEY INSIGHTS",
            "-" * 20,
            *[f"- {insight}" for insight in insights],
            "",
            "Note: Forecasts are simple moving-average estimates.",
        ]

        path.write_text("\n".join(lines), encoding="utf-8")
        print(f"Executive summary saved: {path}")
        return path

    def generate_all(self, analyzer):
        return {
            "excel": self.export_excel(analyzer),
            "csv": self.export_csv_reports(analyzer),
            "summary": self.export_executive_summary(analyzer),
        }
