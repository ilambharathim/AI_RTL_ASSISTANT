"""
Exceptions raised by the RIVA specification-processing frontend.
"""


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
