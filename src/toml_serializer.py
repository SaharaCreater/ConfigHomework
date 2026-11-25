from typing import Any
import tomli_w


def to_toml(data: dict[str, Any]) -> str:
    return tomli_w.dumps(data)
