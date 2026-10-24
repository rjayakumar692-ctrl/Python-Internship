# Week 7 – Sales Data Analysis Dashboard

## Project Overview

The **Sales Data Analysis Dashboard** is a Python-based data analysis project that loads, cleans, analyzes, and visualizes sales data. It generates reports and charts to help understand revenue, product performance, customer purchasing behavior, regional sales, and monthly trends.

## Features

- Load sales data from CSV and Excel files.
- Remove duplicate records and handle invalid data.
- Handle missing values and convert data types.
- Calculate revenue, average order value, and total units sold.
- Analyze sales by category, product, month, customer, and region.
- Generate monthly sales forecasts using a simple moving average.
- Create monthly, category, regional, and dashboard visualizations.
- Export Excel reports, CSV reports, and an executive summary.
- Run automated tests using `pytest`.

## Project Structure

```text
week7/
├── sales_analyzer/
│   ├── __init__.py
│   ├── data_loader.py
│   ├── data_cleaner.py
│   ├── analyzer.py
│   ├── visualizer.py
│   └── reporter.py
├── data/
│   ├── raw/
│   │   └── sales_data.csv
│   ├── processed/
│   └── reports/
├── notebooks/
│   ├── exploration.ipynb
│   └── analysis.ipynb
├── tests/
│   ├── __init__.py
│   ├── test_data_loader.py
│   ├── test_data_cleaner.py
│   └── test_analyzer.py
├── output/
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Technologies Used

- **Python** – Core programming language
- **Pandas and NumPy** – Data processing and analysis
- **Matplotlib** – Data visualization
- **OpenPyXL** – Excel report generation
- **Jupyter Notebook** – Data exploration
- **Pytest** – Automated testing

## Installation

### 1. Clone the repository

If you are downloading this project from GitHub:

```powershell
git clone <your-repository-url>
cd week7
```

Alternatively, open the existing `week7` project folder in VS Code.

### 2. Create and activate a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

## Run the Project

Run the complete workflow:

```powershell
python main.py --action all
```

Run individual analyses:

```powershell
python main.py --action info
python main.py --action stats
python main.py --action categories
python main.py --action products
python main.py --action monthly
python main.py --action customers
python main.py --action regions
python main.py --action forecast
python main.py --action visualize
python main.py --action report
```

To process a different CSV or Excel file:

```powershell
python main.py --file "data/raw/sales_data.csv" --action all
```

Replace the file path with the path to your own dataset when needed.

## Run Automated Tests

Execute the test suite:

```powershell
python -m pytest -v
```

**Latest test result:** 11 tests passed.

## Sample Analysis Results

The project was successfully executed using the supplied sales dataset.

| Metric | Result |
|---|---:|
| Records processed | 32 |
| Total revenue | 8,950 |
| Unique orders | 32 |
| Unique customers | 10 |
| Unique products | 10 |
| Total units sold | 87 |
| Top-performing product | Laptop |
| Highest-revenue category | Electronics |
| Highest-revenue region | East |

*These results describe the current sample dataset. Results will vary when a different dataset is used.*

## Generated Outputs

After running the complete workflow, the project generates:

- **Cleaned dataset:** `data/processed/sales_data_cleaned.csv`
- **Excel report:** `data/reports/sales_analysis_report.xlsx`
- **CSV reports:** `data/reports/`
- **Executive summary:** `data/reports/executive_summary.txt`
- **Charts and dashboard:** `output/`

The visualizations include monthly sales trends, category sales, category share, regional performance, and a combined dashboard.

## Forecast Disclaimer

The sales forecast uses a simple moving-average method for educational purposes. It provides estimates based on historical sales and is not a guarantee of future performance.
## Dashboard Preview

![Sales Analysis Dashboard](output/sales_dashboard.png)