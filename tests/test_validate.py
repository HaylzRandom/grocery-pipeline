import pandas as pd
from pathlib import Path
import pytest
from pipeline.validate import validate


def test_validate_passes(tmp_path):
    path = tmp_path / "valid.csv"
    pd.DataFrame({"a": [1, 2, 3]}).to_csv(path, index=False)

    assert validate(path) is True


def test_validate_missing(tmp_path):
    path = tmp_path / "missing.csv"

    with pytest.raises(FileNotFoundError):
        validate(path)


def test_validate_empty_dataframe(tmp_path):
    # Case: file has headers but no rows
    path = tmp_path / "empty.csv"
    pd.DataFrame(columns=["a", "b"]).to_csv(path, index=False)

    with pytest.raises(ValueError, match="empty"):
        validate(path)


def test_validate_zero_byte_file(tmp_path):
    # Case: file exists but no content
    path = tmp_path / "blank.csv"
    path.write_text("")

    with pytest.raises(ValueError, match="empty"):
        validate(path)
