from toolkit.constants import TYPE_CONVERT, TYPE_L_COEF, TYPE_M_COEF
from toolkit.errors import ToolkitError


def valid_type_convert(type_convert: str) -> str | bool:
    return TYPE_CONVERT[type_convert.lower()] if type_convert.lower() in TYPE_CONVERT else False


def convert(value: str, from_type: str, to_type: str) -> float:

    if not valid_type_convert(from_type) or not valid_type_convert(to_type):
        raise ToolkitError("Ошибка! Неизвестная единица")

    if valid_type_convert(from_type) != valid_type_convert(to_type):
        raise ToolkitError("Ошибка! Несовместимые единицы")

    try:  # ловим ошибку при неверном числовом значении
        value = float(value)
    except (ValueError, TypeError):
        raise ToolkitError("Ошибка! Неверное числовое значение") from None

    if valid_type_convert(from_type) == "l":
        return value * TYPE_L_COEF[from_type.lower()] / TYPE_L_COEF[to_type.lower()]

    elif valid_type_convert(from_type) == "m":
        return value * TYPE_M_COEF[from_type.lower()] / TYPE_M_COEF[to_type.lower()]

    elif valid_type_convert(from_type) == "t":

        if from_type.lower() == "c":

            if value + 273.15 < 0:
                raise ToolkitError("Температура ниже абсолютного нуля запрещена!")

            if to_type.lower() == "c":
                return value

            elif to_type.lower() == "k":
                return value + 273.15

            elif to_type.lower() == "f":
                return value * 9 / 5 + 32

        elif from_type.lower() == "k":

            if value < 0:
                raise ToolkitError("Температура ниже абсолютного нуля запрещена!")

            if to_type.lower() == "c":
                return value - 273.15

            elif to_type.lower() == "k":
                return value

            elif to_type.lower() == "f":
                return (value - 273.15) * 9 / 5 + 32

        elif from_type.lower() == "f":

            if (value - 32) * 5 / 9 + 273.15 < 0:
                raise ToolkitError("Температура ниже абсолютного нуля запрещена!")

            if to_type.lower() == "c":
                return (value - 32) * 5 / 9

            elif to_type.lower() == "k":
                return (value - 32) * 5 / 9 + 273.15

            elif to_type.lower() == "f":
                return value
