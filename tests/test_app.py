from pathlib import Path

import pandas as pd

from app import REQUIRED_COLUMNS, load_data


def test_data_file_exists():
    assert Path("data/ventas.csv").exists()


def test_load_data_has_required_columns():
    data = load_data()
    assert REQUIRED_COLUMNS.issubset(data.columns)
    assert not data.empty
    assert pd.api.types.is_datetime64_any_dtype(data["fecha"])


def test_sales_and_units_are_positive():
    data = load_data()
    assert (data["ventas"] > 0).all()
    assert (data["unidades"] > 0).all()
