import argparse
import sys
from pathlib import Path
from src.parser import ConfigSyntaxError, parse_config
from src.toml_serializer import to_toml

EXIT_SUCCESS = 0
EXIT_ERROR = 1


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Транслятор учебного конфигурационного языка в TOML."
    )
    parser.add_argument(
        "-i",
        "--input",
        required=True,
        help="Путь к входному конфигурационному файлу.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    input_path = Path(args.input)

    if not input_path.is_file():
        print(f"Ошибка: файл '{input_path}' не найден.", file=sys.stderr)
        return EXIT_ERROR

    try:
        content = input_path.read_text(encoding="utf-8")
        parsed_data = parse_config(content)
        sys.stdout.write(to_toml(parsed_data))
        return EXIT_SUCCESS
    except ConfigSyntaxError as exc:
        print(f"Ошибка разбора: {exc}", file=sys.stderr)
        return EXIT_ERROR


if __name__ == "__main__":
    sys.exit(main())
