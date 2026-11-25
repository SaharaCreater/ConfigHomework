import pytest
from src.cli import EXIT_ERROR, EXIT_SUCCESS, main
from src.parser import ConfigSyntaxError, parse_config
from src.toml_serializer import to_toml


def test_comments_and_numbers() -> None:
    src = """
    C Однострочный комментарий
    {
      Многострочный
      комментарий
    }
    def int_like := 42.
    def pi_val := 3.14
    """
    res = parse_config(src)
    assert res == {"int_like": 42.0, "pi_val": 3.14}


def test_strings_and_nested_arrays() -> None:
    src = """
    def greeting := 'Привет, мир'
    def matrix := [ [ 1., 2. ], [ 3., 4. ], [ 'a', 'b' ] ]
    """
    res = parse_config(src)
    assert res["greeting"] == "Привет, мир"
    assert res["matrix"] == [[1.0, 2.0], [3.0, 4.0], ["a", "b"]]


def test_const_expressions_add_and_sort() -> None:
    src = """
    def base := 10.
    def offset := |base + 5.5|
    def raw_arr := [ 30., 10., 20. ]
    def sorted_arr := |sort(raw_arr)|
    def nested_expr := |sort([ |base + 2.|, 1., 5. ])|
    """
    res = parse_config(src)
    assert res["offset"] == 15.5
    assert res["sorted_arr"] == [10.0, 20.0, 30.0]
    assert res["nested_expr"] == [1.0, 5.0, 12.0]


def test_string_concatenation_in_expr() -> None:
    src = """
    def prefix := 'srv_'
    def full_name := |prefix + 'prod'|
    def merged := |[ 1. ] + [ 2. ]|
    """
    res = parse_config(src)
    assert res["full_name"] == "srv_prod"
    assert res["merged"] == [1.0, 2.0]


def test_syntax_and_semantic_errors() -> None:
    with pytest.raises(ConfigSyntaxError):
        parse_config("def 1bad := 10.")

    with pytest.raises(ConfigSyntaxError):
        parse_config("def x := |unknown + 1.|")

    with pytest.raises(ConfigSyntaxError):
        parse_config("def x := |sort(10.)|")


def test_cli_and_toml_output(tmp_path, capsys) -> None:
    cfg_file = tmp_path / "test.conf"
    cfg_file.write_text("def port := 8080.\ndef host := 'localhost'\n")

    code = main(["-i", str(cfg_file)])
    captured = capsys.readouterr()

    assert code == EXIT_SUCCESS
    assert "port = 8080.0" in captured.out
    assert 'host = "localhost"' in captured.out
    assert "port = 8080.0" in to_toml({"port": 8080.0})

    err_code = main(["-i", str(tmp_path / "missing.conf")])
    assert err_code == EXIT_ERROR
