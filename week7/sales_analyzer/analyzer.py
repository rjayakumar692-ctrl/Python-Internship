
import pandas as pd


class SalesAnalyzer:
    """Perform sales analysis and generate business insights."""

    def __init__(self, df):
        self.df = df.copy()

        if self.df.empty:
            raise ValueError("Cannot analyze an empty DataFrame.")

    def calculate_basic_stats(self):
        df = self.df

        return {
            "total_records": int(len(df)),
            "total_revenue": round(float(df["total_amount"].sum()), 2),
            "total_orders": int(df["order_id"].nunique()),
            "unique_customers": int(df["customer_id"].nunique()),
            "unique_products": int(df["product_id"].nunique()),
            "total_units_sold": int(df["quantity"].sum()),
            "average_order_value": round(
                float(df.groupby("order_id")["total_amount"].sum().mean()), 2
            ),
            "average_sale": round(float(df["total_amount"].mean()), 2),
        }

    def sales_by_category(self):
        result = (
            self.df.groupby("category", dropna=False)
            .agg(
                total_sales=("total_amount", "sum"),
                units_sold=("quantity", "sum"),
                orders=("order_id", "nunique"),
            )
            .sort_values("total_sales", ascending=False)
            .reset_index()
        )
        result["total_sales"] = result["total_sales"].round(2)
        return result

    def top_products(self, n=5):
        return (
            self.df.groupby(["product_id", "product_name"], dropna=False)
            .agg(
                total_sales=("total_amount", "sum"),
                units_sold=("quantity", "sum"),
            )
            .sort_values("total_sales", ascending=False)
            .head(n)
            .reset_index()
        )

    def monthly_sales(self):
        df = self.df.copy()
        df["month_year"] = df["order_date"].dt.to_period("M").astype(str)

        result = (
            df.groupby("month_year")
            .agg(
                total_sales=("total_amount", "sum"),
                orders=("order_id", "nunique"),
            )
            .sort_index()
            .reset_index()
        )

        result["monthly_growth_percent"] = (
            result["total_sales"].pct_change() * 100
        ).round(2)

        result["total_sales"] = result["total_sales"].round(2)
        return result

    def sales_by_region(self):
        return (
            self.df.groupby("region", dropna=False)
            .agg(
                total_sales=("total_amount", "sum"),
                orders=("order_id", "nunique"),
            )
            .sort_values("total_sales", ascending=False)
            .reset_index()
        )

    def customer_analysis(self):
        result = (
            self.df.groupby("customer_id", dropna=False)
            .agg(
                total_spent=("total_amount", "sum"),
                orders=("order_id", "nunique"),
                units_bought=("quantity", "sum"),
                last_purchase=("order_date", "max"),
            )
            .sort_values("total_spent", ascending=False)
            .reset_index()
        )
        result["total_spent"] = result["total_spent"].round(2)
        return result

    def peak_sales_period(self):
        monthly = self.monthly_sales()

        if monthly.empty:
            return None

        return monthly.loc[monthly["total_sales"].idxmax()].to_dict()

    def monthly_sales_forecast(self, periods=3):
        """Simple moving-average forecast using the last 3 observed months."""
        monthly = self.monthly_sales()

        if periods < 1:
            raise ValueError("periods must be at least 1")

        if monthly.empty:
            return pd.DataFrame(
                columns=["month_year", "forecast_sales"]
            )

        values = monthly["total_sales"].astype(float)
        window = min(3, len(values))
        average = float(values.tail(window).mean())

        last_month = pd.Period(monthly["month_year"].iloc[-1], freq="M")
        future_months = [
            str(last_month + i) for i in range(1, periods + 1)
        ]

        return pd.DataFrame({
            "month_year": future_months,
            "forecast_sales": [round(average, 2)] * periods,
        })

    def generate_insights(self):
        stats = self.calculate_basic_stats()
        categories = self.sales_by_category()
        products = self.top_products(1)
        monthly = self.monthly_sales()
        regions = self.sales_by_region()

        insights = [
            f"Total revenue: {stats['total_revenue']:.2f}",
            f"Unique orders: {stats['total_orders']}",
            f"Unique customers: {stats['unique_customers']}",
        ]

        if not categories.empty:
            row = categories.iloc[0]
            insights.append(
                f"Top category: {row['category']} "
                f"({row['total_sales']:.2f} in sales)"
            )

        if not products.empty:
            row = products.iloc[0]
            insights.append(
                f"Top product: {row['product_name']} "
                f"({row['total_sales']:.2f} in sales)"
            )

        if not monthly.empty:
            row = monthly.loc[monthly["total_sales"].idxmax()]
            insights.append(
                f"Best sales month: {row['month_year']} "
                f"({row['total_sales']:.2f})"
            )

        if not regions.empty:
            row = regions.iloc[0]
            insights.append(
                f"Top region: {row['region']} "
                f"({row['total_sales']:.2f} in sales)"
            )

        return insights
