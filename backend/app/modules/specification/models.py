"""
Specification Data Models

These models represent the structured information extracted
from a hardware specification document.
"""

from dataclasses import dataclass, field

from app.modules.specification.requirement_rule import RequirementRule


@dataclass
class SpecificationModel:
    """
    Represents the complete parsed specification.
    """

    # -------------------------------
    # Basic Information
    # -------------------------------

    module_name: str = ""

    # -------------------------------
    # Module Interface
    # -------------------------------

    inputs: list[str] = field(default_factory=list)

    outputs: list[str] = field(default_factory=list)

    # -------------------------------
    # Functional Requirements
    # -------------------------------

    requirements: list[RequirementRule] = field(default_factory=list)