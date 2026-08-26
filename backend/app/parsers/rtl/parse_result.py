"""
Compatibility module for the RTL parser result.

The canonical RTL parser result is RTLParserResult from
parser_result.py.

This module remains available for compatibility with any external
imports that may still reference app.parsers.rtl.parse_result.
"""

from app.parsers.rtl.parser_result import RTLParserResult


RTLParseResult = RTLParserResult


__all__ = [
    "RTLParseResult",
]
