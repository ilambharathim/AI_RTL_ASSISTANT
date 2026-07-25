"""
Exceptions raised by the RIVA specification-processing frontend.
"""

from app.parsers.specification.parser_diagnostic_code import (
    SpecificationParserDiagnosticCode,
)


class SpecificationParserError(Exception):
    """
    Base exception for specification frontend failures.
    """


class SpecificationReadError(SpecificationParserError):
    """
    Raised when a specification document cannot be read.
    """


class UnsupportedSpecificationFormatError(SpecificationReadError):
    """
    Raised when no reader exists for a specification file format.
    """


class SpecificationTokenStreamError(SpecificationParserError):
    """
    Raised when a parser receives an invalid or incomplete token stream.
    """


class SpecificationSyntaxError(SpecificationParserError):
    """
    Raised when a valid token stream violates the generic document grammar.
    """

    def __init__(
        self,
        message: str,
        *,
        code: SpecificationParserDiagnosticCode = (
            SpecificationParserDiagnosticCode.UNEXPECTED_TOKEN
        ),
        line: int,
        column: int,
        source_file: str = "",
    ) -> None:
        if not isinstance(code, SpecificationParserDiagnosticCode):
            raise TypeError(
                "code must be a SpecificationParserDiagnosticCode."
            )

        if not isinstance(message, str) or not message:
            raise ValueError("message must be a non-empty string.")

        if not isinstance(line, int) or line < 1:
            raise ValueError("line must be an integer greater than or equal to 1.")

        if not isinstance(column, int) or column < 1:
            raise ValueError(
                "column must be an integer greater than or equal to 1."
            )

        if not isinstance(source_file, str):
            raise TypeError("source_file must be a string.")

        self.code = code.value
        self.message = message
        self.line = line
        self.column = column
        self.source_file = source_file

        location = source_file or "<memory>"
        super().__init__(f"{location}:{line}:{column}: {message}")
