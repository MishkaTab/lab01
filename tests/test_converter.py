import pytest

from toolkit.converter import convert
from toolkit.errors import ToolkitError


def test_negative_diff_types() -> None:

    with pytest.raises(ToolkitError):
        convert("67", "m", "kg")


def test_negative_wrong_types() -> None:

    with pytest.raises(ToolkitError):
        convert("52", "l", "N")


def test_negative_so_cold() -> None:

    with pytest.raises(ToolkitError):
        convert("-280", "c", "k")


def test_convert_len() -> None:

    assert convert("1000", "cm", "m") == 10
    assert convert("1.3", "km", "cm") == 130000
    assert convert("0.1", "cm", "mm") == 1


def test_convert_mas() -> None:

    assert convert("1000", "g", "kg") == 1
    assert convert("1.2", "kg", "g") == 1200


def test_convert_temp() -> None:

    assert convert("20", "c", "c") == 20
    assert convert("100", "c", "k") == 373.15
