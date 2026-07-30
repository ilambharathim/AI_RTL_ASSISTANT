"""
Kinds of semantic scopes.
"""

from enum import Enum


class ScopeKind(str, Enum):

    GLOBAL = "GLOBAL"

    MODULE = "MODULE"

    PROCEDURAL = "PROCEDURAL"

    CONDITIONAL = "CONDITIONAL"

    LOOP = "LOOP"

    GENERATE = "GENERATE"

    FUNCTION = "FUNCTION"

    TASK = "TASK"
