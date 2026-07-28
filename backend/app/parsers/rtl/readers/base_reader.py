"""
Base interface for deterministic RTL token readers.

Every reader is responsible for recognizing and consuming one
lexical construct from the CharacterStream.
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from app.domain.rtl_tokens import RTLToken
from app.engines.diagnostics.diagnostic import Diagnostic
from app.parsers.rtl.character_stream import CharacterStream


class BaseReader(ABC):
    """
    Abstract base class for all lexer readers.
    """

    @staticmethod
    @abstractmethod
    def matches(
        stream: CharacterStream,
    ) -> bool:
        """
        Return True if this reader can consume the next token.
        """

    @staticmethod
    @abstractmethod
    def read(
        stream: CharacterStream,
        diagnostics: list[Diagnostic],
    ) -> RTLToken | None:
        """
        Consume one lexical construct.

        Returns:
            RTLToken if a token was produced.

            None if the reader intentionally produced no token
            (for example comments).

        Readers should never raise exceptions for malformed user
        source code. Instead they append Diagnostic objects to
        the diagnostics list whenever possible.
        """
