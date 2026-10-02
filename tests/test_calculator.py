import pytest

from toolkit.errors import ToolkitError
from toolkit.validate import is_correct_token, validate
from toolkit.calculator import calculate, to_rpn


def test_negative_validate() -> None:

    with pytest.raises(ToolkitError):
        validate([" "])


def test_negative_validate_parentheses() -> None:

    with pytest.raises(ToolkitError):
        is_correct_token(["(", "(", "5", "+", "6.7", ")"])


def test_negative_number() -> None:

    with pytest.raises(ToolkitError):
        validate(["5", "*", "@"])


def test_negative_pow() -> None:

    with pytest.raises(ToolkitError):
        is_correct_token(["6", "*", "*", "7"])


def test_negative_dev_by_zero() -> None:

    with pytest.raises(ToolkitError):
        calculate(["5", "0", "/"])


def test_to_rpn() -> None:

    tokens = ["5", "+", "8", "*", "u-", "(", "6.7", "/", "0.52", ")"]

    assert to_rpn(tokens) == ["5", "8", "6.7", "0.52", "/", "u-", "*", "+"]


def test_calculator_pow() -> None:

    tokens = ["2", "5", "^"]

    assert calculate(tokens) == 32
    assert calculate(["2", "2", "u-", "^"]) == 0.25


def test_negative_double_bin_operation() -> None:

    with pytest.raises(ToolkitError):
        is_correct_token(["5", "+", "*", "10"])
