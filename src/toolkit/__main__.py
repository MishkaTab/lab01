import argparse
import sys

from toolkit.errors import ToolkitError
from toolkit.tokenize import tokenize
from toolkit.validate import validate
from toolkit.calculator import to_rpn, calculate
from toolkit.converter import convert


def create_parser():

    parser = argparse.ArgumentParser(description="Калькулятор и конвертер")

    mode_of_operations = parser.add_subparsers(
        dest="mode", required=True
    )  # обязательный выбор команд, создаём доп парсер, чтобы разделять режимы (mode) работы
    calc_parser = mode_of_operations.add_parser("calc")
    convert_parser = mode_of_operations.add_parser("convert")

    calc_parser.add_argument("expression")  # обязательные аргументы для calc

    convert_parser.add_argument("value")  # обязательные аргументы для covert
    convert_parser.add_argument("--from", dest="from_type", required=True)
    convert_parser.add_argument("--to", dest="to_type", required=True)

    return parser


def main():

    parser = create_parser()
    argv = sys.argv[1:]

    if len(argv) == 2 and argv[0] == "calc" and argv[1] not in ("-h", "--help"):
        argv.insert(1, "--")

    args = parser.parse_args(argv)

    try:
        if args.mode == "calc":
            tokens = tokenize(args.expression)
            validate(tokens)
            rpn = to_rpn(tokens)
            result = calculate(rpn)
        else:
            result = convert(args.value, args.from_type, args.to_type)

    except ToolkitError as error:
        print(str(error), file=sys.stderr)
        return 2

    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
