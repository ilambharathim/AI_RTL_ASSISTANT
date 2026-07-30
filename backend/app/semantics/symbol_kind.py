"""
Kinds of compiler symbols.
"""

from enum import Enum


class SymbolKind(str, Enum):

    MODULE = "MODULE"

    PORT = "PORT"

    SIGNAL = "SIGNAL"

    PARAMETER = "PARAMETER"

    LOCALPARAM = "LOCALPARAM"

    FUNCTION = "FUNCTION"

    TASK = "TASK"

    GENVAR = "GENVAR"
