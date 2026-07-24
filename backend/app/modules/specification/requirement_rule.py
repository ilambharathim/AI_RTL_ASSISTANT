"""
Requirement Rule Model

Represents a single functional rule extracted
from the specification.
"""

from dataclasses import dataclass


@dataclass
class RequirementRule:
    """
    Represents one functional requirement.
    """

    condition: str
    output_signal: str
    expected_value: str