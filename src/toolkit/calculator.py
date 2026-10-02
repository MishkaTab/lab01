from toolkit.constants import BINARY_OPERATORS, UNARY_OPERATORS
from toolkit.constants import PRIORITIES as prty
from toolkit.validate import is_number
from toolkit.errors import ToolkitError


def priority(token: str) -> int | bool:

    return prty[token] if token in prty else False


def to_rpn(tokens: list[str]) -> list[str]:
    oper_stack = ["("]
    rpn = []

    for token in tokens + [")"]:
        if is_number(token):
            rpn.append(token)

        elif token in ("(",) + UNARY_OPERATORS:
            oper_stack.append(token)

        elif token == ")":
            while oper_stack and oper_stack[-1] != "(":
                rpn.append(oper_stack.pop())
            oper_stack.pop()

        elif token in BINARY_OPERATORS:
            while (
                oper_stack
                and oper_stack[-1] != "("
                and (
                    priority(token) < priority(oper_stack[-1])
                    or priority(token) == priority(oper_stack[-1])
                    and token != "^"
                )
            ):  # ^-правоассоциативна
                rpn.append(oper_stack.pop())

            oper_stack.append(token)

    return rpn


def calculate(rpn: list[str]) -> float:

    number_stack = []

    for el in rpn:
        if is_number(el):
            number_stack.append(float(el))

        elif el == "u-":
            number_stack[-1] *= -1
        elif el == "u+":  # явно покажем, что при унарном + знак не меняется
            continue

        elif el == "+":
            right_num = number_stack.pop()
            left_num = number_stack.pop()

            number_stack.append(left_num + right_num)

        elif el == "-":
            right_num = number_stack.pop()
            left_num = number_stack.pop()

            number_stack.append(left_num - right_num)

        elif el == "*":
            right_num = number_stack.pop()
            left_num = number_stack.pop()

            number_stack.append(left_num * right_num)

        elif el == "/":
            right_num = number_stack.pop()
            left_num = number_stack.pop()

            if right_num == 0:
                raise ToolkitError("Ошибка! Деление на 0")

            number_stack.append(left_num / right_num)

        elif el == "%":
            right_num = number_stack.pop()
            left_num = number_stack.pop()

            if right_num == 0.0:
                raise ToolkitError("Ошибка! Деление на 0")

            number_stack.append(left_num % right_num)

        elif el == "^":
            right_num = number_stack.pop()
            left_num = number_stack.pop()

            if left_num == 0 and right_num < 0:
                raise ToolkitError("Неявное деления на ноль! Попытка возвести ноль в отрицательную степень")
            elif left_num < 0 and right_num != int(right_num):
                raise ToolkitError(f"Данный калькулятор не поддерживает комплексные числа - {left_num}^{right_num}")

            try:
                number_stack.append(left_num**right_num)
            except OverflowError:
                raise ToolkitError("Слишком большой результат") from None

    return number_stack.pop()
