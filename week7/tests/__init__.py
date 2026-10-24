
import pandas as pd
import pytest

from sales_analyzer.data_loader import SalesDataLoader


def test_load_sample_csv():
    loader = SalesDataLoader()
    df = loader.load_data("data/raw/sales_data.csv")

    assert not df.empty
    assert "order_date" in df.columns
    assert "total_amount" in df.columns


def test_missing_file_raises_error():
    loader = SalesDataLoader()

    with pytest.raises(FileNotFoundError):
        loader.load_data("data/raw/does_not_exist.csv")


def test_unsupported_extension_raises_error(tmp_path):
    path = tmp_path / "sales.txt"
    path.write_text("sample", encoding="utf-8")

    with pytest.raises(ValueError):
        SalesDataLoader().load_data(path)
