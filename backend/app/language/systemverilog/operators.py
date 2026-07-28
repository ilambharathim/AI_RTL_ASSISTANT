"""
SystemVerilog operators.

Single source of truth for every lexical operator recognised by RIVA.

Operators are grouped by token length because the lexer follows the
longest-match rule (maximal munch).
"""

# ---------------------------------------------------------------------
# Single-character operators
# ---------------------------------------------------------------------

OPERATORS_1 = frozenset(
    {
        "+",
        "-",
        "*",
        "/",
        "%",
        "=",
        "<",
        ">",
        "!",
        "&",
        "|",
        "^",
        "~",
        "?",
    }
)

# ---------------------------------------------------------------------
# Two-character operators
# ---------------------------------------------------------------------

OPERATORS_2 = frozenset(
    {
        "==",
        "!=",
        "<=",
        ">=",
        "&&",
        "||",
        "<<",
        ">>",
        "+=",
        "-=",
        "*=",
        "/=",
        "%=",
        "&=",
        "|=",
        "^=",
        "->",
        "=>",
        "::",
        "++",
        "--",
    }
)

# ---------------------------------------------------------------------
# Three-character operators
# ---------------------------------------------------------------------

OPERATORS_3 = frozenset(
    {
        "===",
        "!==",
        "<<<",
        ">>>",
        "<<=",
        ">>=",
    }
)

# ---------------------------------------------------------------------
# Four-character operators
# ---------------------------------------------------------------------

OPERATORS_4 = frozenset(
    {
        "<<<=",
        ">>>=",
    }
)

SYSTEMVERILOG_OPERATORS = (
    OPERATORS_4
    | OPERATORS_3
    | OPERATORS_2
    | OPERATORS_1
)
