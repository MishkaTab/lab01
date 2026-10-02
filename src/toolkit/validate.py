from toolkit.constants import VALID_CHARS, BINARY_OPERATORS, NUMBER_PAT, UNARY_OPERATORS
from toolkit.constants import WRONG_PAT as wrong_pat
from toolkit.errors import ToolkitError
import re


def is_number(token: str) -> bool:
    return re.fullmatch(NUMBER_PAT, token) is not None


def is_operation(token: str) -> bool:
    return token in BINARY_OPERATORS


def is_un_operation(token: str) -> bool:
    return token in UNARY_OPERATORS


def is_correct_token(tokens: list[str]) -> None:
    # num - число, oper - операция
    c_par = 0  # счётчик скобочек "(" - +1, ")" - -1. Если в конце 0, то верно
    state = "number"  # состояние: ждём оператор или операнд

    if re.findall(wrong_pat, "".join(tokens)):
        raise ToolkitError("Некорректная скобочная комбинация! Пропущен операнд или операция")

    for token in tokens:

        if token == "(":
            c_par += 1
        elif token == ")":
            c_par -= 1
        if c_par < 0:
            raise ToolkitError("Неверная комбинация скобочек")

        if is_operation(token) and state == "number":
            raise ToolkitError("Пропущен операнд")
        elif is_number(token) and state == "operation":
            raise ToolkitError("Пропущена операция")
        elif is_operation(token) and state == "operation":
            state = "number"
        elif is_number(token) and state == "number":
            state = "operation"
        elif is_un_operation(token) and state != "number":
            raise ToolkitError("Унарный знак находится после операнда")

    if c_par != 0:
        raise ToolkitError("Неверная комбинация скобочек")

    return None


def validate(tokens: list[str]) -> None:
    if not tokens:
        raise ToolkitError("Упс, кажется, вы забыли ввести выражение")  # пустое вырыжение (п1)

    for token in tokens:
        wrong_chars = [char for char in token if char not in VALID_CHARS]
        if wrong_chars:
            raise ToolkitError(
                f"Недопустимый элемент(ы) - {wrong_chars}\nДробные числа вводите через точку"
            )  # недопустимый элемент (п2)

        if not (is_number(token) or is_operation(token) or token in ("(", ")") or is_un_operation(token)):
            raise ToolkitError(f"Некорректная запись числа - {token}")

    is_correct_token(tokens)

    if not (is_number(tokens[-1]) or tokens[-1] == ")"):
        raise ToolkitError("Неверная последовательнось! В конце не число и не закрывающаяся скобка")
