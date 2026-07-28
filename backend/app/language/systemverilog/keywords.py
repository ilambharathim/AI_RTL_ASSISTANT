"""
SystemVerilog reserved keywords.

Single source of truth for every reserved keyword used by RIVA.
"""

from app.language.systemverilog.keyword_categories.design_units import DESIGN_UNIT_KEYWORDS
from app.language.systemverilog.keyword_categories.declarations import DECLARATION_KEYWORDS
from app.language.systemverilog.keyword_categories.data_types import DATA_TYPE_KEYWORDS
from app.language.systemverilog.keyword_categories.procedural import PROCEDURAL_KEYWORDS
from app.language.systemverilog.keyword_categories.oop import OOP_KEYWORDS
from app.language.systemverilog.net_types import NET_TYPE_KEYWORDS

SYSTEMVERILOG_KEYWORDS: dict[str, None] = {}

for category in (
    DESIGN_UNIT_KEYWORDS,
    DECLARATION_KEYWORDS,
    DATA_TYPE_KEYWORDS,
    NET_TYPE_KEYWORDS,
    PROCEDURAL_KEYWORDS,
    OOP_KEYWORDS,
):
    duplicate = SYSTEMVERILOG_KEYWORDS.keys() & category.keys()

    if duplicate:
        raise ValueError(
            f"Duplicate SystemVerilog keywords: {sorted(duplicate)}"
        )

    SYSTEMVERILOG_KEYWORDS.update(category)
