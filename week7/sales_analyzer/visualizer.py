
from pathlib import Path
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt


class SalesVisualizer:
    """Create and save sales charts."""

    def __init__(self, output_dir="output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def monthly_sales_chart(self, monthly):
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(
            monthly["month_year"], monthly["total_sales"],
            marker="o"
        )
        ax.set_title("Monthly Sales Trend")
        ax.set_xlabel("Month")
        ax.set_ylabel("Sales")
        ax.tick_params(axis="x", rotation=45)
        ax.grid(True, alpha=0.3)
        fig.tight_layout()
        path = self.output_dir / "monthly_sales.png"
        fig.savefig(path, dpi=150)
        plt.close(fig)
        return path

    def category_sales_chart(self, categories):
        fig, ax = plt.subplots(figsize=(9, 5))
        ax.bar(categories["category"], categories["total_sales"])
        ax.set_title("Sales by Category")
        ax.set_xlabel("Category")
        ax.set_ylabel("Sales")
        ax.tick_params(axis="x", rotation=30)
        fig.tight_layout()
        path = self.output_dir / "category_sales.png"
        fig.savefig(path, dpi=150)
        plt.close(fig)
        return path

    def category_pie_chart(self, categories):
        fig, ax = plt.subplots(figsize=(7, 7))
        if categories["total_sales"].sum() > 0:
            ax.pie(
                categories["total_sales"],
                labels=categories["category"],
                autopct="%1.1f%%",
                startangle=90,
            )
        ax.set_title("Revenue Share by Category")
        fig.tight_layout()
        path = self.output_dir / "category_share.png"
        fig.savefig(path, dpi=150)
        plt.close(fig)
        return path

    def regional_sales_chart(self, regions):
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.bar(regions["region"], regions["total_sales"])
        ax.set_title("Sales by Region")
        ax.set_xlabel("Region")
        ax.set_ylabel("Sales")
        fig.tight_layout()
        path = self.output_dir / "regional_sales.png"
        fig.savefig(path, dpi=150)
        plt.close(fig)
        return path

    def create_dashboard(self, monthly, categories, regions):
        fig, axes = plt.subplots(2, 2, figsize=(14, 9))

        axes[0, 0].plot(
            monthly["month_year"], monthly["total_sales"], marker="o"
        )
        axes[0, 0].set_title("Monthly Sales")
        axes[0, 0].tick_params(axis="x", rotation=45)

        axes[0, 1].bar(
            categories["category"], categories["total_sales"]
        )
        axes[0, 1].set_title("Sales by Category")
        axes[0, 1].tick_params(axis="x", rotation=30)

        if categories["total_sales"].sum() > 0:
            axes[1, 0].pie(
                categories["total_sales"],
                labels=categories["category"],
                autopct="%1.1f%%",
            )
        axes[1, 0].set_title("Category Share")

        axes[1, 1].bar(
            regions["region"], regions["total_sales"]
        )
        axes[1, 1].set_title("Sales by Region")

        fig.suptitle("Sales Analysis Dashboard", fontsize=16)
        fig.tight_layout()
        path = self.output_dir / "sales_dashboard.png"
        fig.savefig(path, dpi=150)
        plt.close(fig)
        return path

    def generate_all(self, analyzer):
        monthly = analyzer.monthly_sales()
        categories = analyzer.sales_by_category()
        regions = analyzer.sales_by_region()

        paths = [
            self.monthly_sales_chart(monthly),
            self.category_sales_chart(categories),
            self.category_pie_chart(categories),
            self.regional_sales_chart(regions),
            self.create_dashboard(monthly, categories, regions),
        ]

        for path in paths:
            print(f"Chart saved: {path}")

        return paths
