"""
Base interface for deterministic preprocessor directive handlers.
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from app.preprocessors.rtl.macro_table import MacroTable


class BaseDirectiveHandler(ABC):

    @staticmethod
    @abstractmethod
    def matches(
        line: str,
    ) -> bool:
        """
        Returns True if this handler owns the directive.
        """

    @staticmethod
    @abstractmethod
    def handle(
        line: str,
        macro_table: MacroTable,
        enabled_stack: list[bool],
    ) -> bool:
        """
        Process one directive.

        Returns True when the directive was consumed.
        """
