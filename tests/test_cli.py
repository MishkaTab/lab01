import subprocess
import sys


def test_cli_calculator() -> None:

    result = subprocess.run(
        [sys.executable, "-m", "toolkit", "calc", "2+3*4"],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert result.stdout.strip() == "14.0"
    assert result.stderr == ""


def test_cli_converter() -> None:

    result = subprocess.run(
        [sys.executable, "-m", "toolkit", "convert", "100", "--from", "cm", "--to", "m"],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert result.stdout.strip() == "1.0"
    assert result.stderr == ""


def test_cli_help() -> None:

    result = subprocess.run(
        [sys.executable, "-m", "toolkit", "--help"],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "calc" in result.stdout
    assert "convert" in result.stdout
    assert result.stderr == ""


def test_cli_division_by_zero() -> None:

    result = subprocess.run(
        [sys.executable, "-m", "toolkit", "calc", "1/0"],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 2
    assert result.stdout == ""
    assert "Деление на 0" in result.stderr
    assert "Traceback" not in result.stderr


def test_cli_missing_expression() -> None:

    result = subprocess.run(
        [sys.executable, "-m", "toolkit", "calc"],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 2
    assert result.stdout == ""
    assert result.stderr
    assert "Traceback" not in result.stderr
