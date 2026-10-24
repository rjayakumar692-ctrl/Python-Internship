
from pathlib import Path

from sales_analyzer.data_loader import SalesDataLoader


def test_load_csv():
    data_path = Path("data/raw/sales_data.csv")

    loader = SalesDataLoader()
    df = loader.load_data(data_path)

    assert not df.empty
    assert "order_id" in df.columns
    assert "total_amount" in df.columns


def test_missing_file():
    loader = SalesDataLoader()

    try:
        loader.load_data("data/raw/missing_file.csv")
        assert False, "Expected FileNotFoundError"
    except FileNotFoundError:
        pass


def test_unsupported_extension(tmp_path):
    file_path = tmp_path / "sales.txt"
    file_path.write_text("test", encoding="utf-8")

    loader = SalesDataLoader()

    try:
        loader.load_data(file_path)
        assert False, "Expected ValueError"
    except ValueError:
        pass
