CONFIG_GRAMMAR = r"""
    start: statement*

    ?statement: const_decl
              | value -> root_value

    const_decl: "def" NAME ":=" value

    ?value: NUMBER          -> number
          | STRING          -> string
          | array
          | const_expr

    array: "[" [value ("," value)*] "]"

    const_expr: "|" expr "|"

    ?expr: expr "+" term    -> add
         | term

    ?term: "sort" "(" expr ")" -> sort_func
         | NAME                -> var_ref
         | NUMBER              -> number
         | STRING              -> string
         | array
         | "(" expr ")"

    NAME: /[_a-zA-Z][_a-zA-Z0-9]*/
    NUMBER: /\d+\.\d*/
    STRING: /'[^']*'/

    LINE_COMMENT: /C(?=[ \t\r\n]|$)[^\r\n]*/
    MULTI_COMMENT: /\{[\s\S]*?\}/

    %import common.WS
    %ignore WS
    %ignore LINE_COMMENT
    %ignore MULTI_COMMENT
"""
