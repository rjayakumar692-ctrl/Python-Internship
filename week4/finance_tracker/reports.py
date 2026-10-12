from collections import defaultdict


class Reports:

    @staticmethod
    def monthly_summary(expenses, year, month):
        monthly_expenses = [
            expense
            for expense in expenses
            if int(expense.date[:4]) == year
            and int(expense.date[5:7]) == month
        ]

        total = sum(expense.amount for expense in monthly_expenses)

        return {
            "count": len(monthly_expenses),
            "total": total,
            "average": total / len(monthly_expenses)
            if monthly_expenses else 0
        }

    @staticmethod
    def category_breakdown(expenses):
        breakdown = defaultdict(float)

        for expense in expenses:
            breakdown[expense.category] += expense.amount

        return dict(sorted(
            breakdown.items(),
            key=lambda item: item[1],
            reverse=True
        ))

    @staticmethod
    def display_category_chart(expenses):
        breakdown = Reports.category_breakdown(expenses)

        if not breakdown:
            print("No expenses available.")
            return

        print("\nCATEGORY BREAKDOWN")
        print("-" * 50)

        maximum = max(breakdown.values())

        for category, amount in breakdown.items():
            bar_length = int((amount / maximum) * 30)
            bar = "#" * bar_length

            print(f"{category:<15} {bar} ₹{amount:.2f}")

    @staticmethod
    def display_monthly_report(expenses, year, month):
        summary = Reports.monthly_summary(expenses, year, month)

        print("\nMONTHLY REPORT")
        print("-" * 40)
        print(f"Month       : {year}-{month:02d}")
        print(f"Transactions: {summary['count']}")
        print(f"Total       : ₹{summary['total']:.2f}")
        print(f"Average     : ₹{summary['average']:.2f}")