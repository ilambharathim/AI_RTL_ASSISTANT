"""
Immutable preprocessor directive model.
"""

from dataclasses import dataclass

from app.preprocessors.rtl.directive_type import RTLDirectiveType


@dataclass(frozen=True, slots=True)
class RTLDirective:

    directive_type: RTLDirectiveType

    text: str

    line: int
