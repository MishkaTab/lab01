from toolkit.constants import BINARY_OPERATORS, UNARY_OPERATORS


def tokenize(line: str) -> list[str]:
    tokens = []
    number = ""
    for char in line:
        if char.isspace():
            if number:
                tokens.append(number)
                number = ""
        elif char in "0123456789.":
            number += char
        else:
            if number:
                tokens.append(number)
                number = ""
            if char in "+-" and (not tokens or tokens[-1] in BINARY_OPERATORS + ("(",) + UNARY_OPERATORS):
                tokens.append("u" + char)  ###так мы будем отличать унарный +-
            else:
                tokens.append(char)
    if number:
        tokens.append(number)

    return tokens
