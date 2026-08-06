"""
IEEE Std 1800-2023 reserved keyword database.

Automatically built from the canonical keyword taxonomy.
"""

from app.language.systemverilog.keywords import (
    SYSTEMVERILOG_KEYWORDS,
)

IEEE1800_2023_RESERVED_KEYWORDS: frozenset[str] = frozenset(
    SYSTEMVERILOG_KEYWORDS.keys()
)
