"""
Supported SystemVerilog preprocessor directives.
"""

from enum import Enum


class RTLDirectiveType(str, Enum):

    DEFINE = "define"
    UNDEF = "undef"

    IFDEF = "ifdef"
    IFNDEF = "ifndef"
    ELSIF = "elsif"
    ELSE = "else"
    ENDIF = "endif"

    INCLUDE = "include"

    UNKNOWN = "unknown"
