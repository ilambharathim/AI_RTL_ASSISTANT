"""
Base parser interface.
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from app.parsers.rtl.parser_context import ParserContext


class BaseParser(ABC):

    @staticmethod
    @abstractmethod
    def matches(
        context: ParserContext,
    ) -> bool:
        ...

    @staticmethod
    @abstractmethod
    def parse(
        context: ParserContext,
    ):
        ...
