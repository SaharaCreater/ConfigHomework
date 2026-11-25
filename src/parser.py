from typing import Any
from lark import Lark, Transformer, v_args
from lark.exceptions import LarkError
from src.grammar import CONFIG_GRAMMAR

MIN_ARGS_COUNT = 1


class ConfigSyntaxError(Exception):
    pass


@v_args(inline=True)
class ConfigTransformer(Transformer):

    def __init__(self) -> None:
        super().__init__()
        self.constants: dict[str, Any] = {}
        self.root_items: list[Any] = []

    def number(self, token: Any) -> float:
        return float(str(token))

    def string(self, token: Any) -> str:
        raw = str(token)
        return raw[MIN_ARGS_COUNT:-MIN_ARGS_COUNT]

    def array(self, *items: Any) -> list[Any]:
        return list(items)

    def var_ref(self, token: Any) -> Any:
        name = str(token)
        if name not in self.constants:
            raise ConfigSyntaxError(f"Неизвестная константа: {name}")
        return self.constants[name]

    def add(self, left: Any, right: Any) -> Any:
        try:
            return left + right
        except TypeError as exc:
            raise ConfigSyntaxError(
                f"Несовместимые типы для сложения: {type(left)} и {type(right)}"
            ) from exc

    def sort_func(self, target: Any) -> list[Any]:
        if not isinstance(target, list):
            raise ConfigSyntaxError("Функция sort() ожидает массив")
        try:
            return sorted(target)
        except TypeError as exc:
            raise ConfigSyntaxError(
                "Элементы массива несравнимы для сортировки"
            ) from exc

    def const_expr(self, result: Any) -> Any:
        return result

    def const_decl(self, name_token: Any, val: Any) -> None:
        self.constants[str(name_token)] = val

    def root_value(self, val: Any) -> None:
        self.root_items.append(val)

    def start(self, *_: Any) -> dict[str, Any]:
        result = dict(self.constants)
        if self.root_items:
            result["values"] = self.root_items
        return result


def parse_config(text: str) -> dict[str, Any]:
    parser = Lark(CONFIG_GRAMMAR, parser="lalr")
    try:
        tree = parser.parse(text)
        transformer = ConfigTransformer()
        return transformer.transform(tree)
    except ConfigSyntaxError:
        raise
    except LarkError as exc:
        raise ConfigSyntaxError(f"Синтаксическая ошибка: {exc}") from exc
