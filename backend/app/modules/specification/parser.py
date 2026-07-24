"""
Specification Parser

Converts raw specification text into a structured SpecificationModel.
"""

import re

from app.modules.specification.models import SpecificationModel
from app.modules.specification.requirement_rule import RequirementRule


class SpecificationParser:
    """
    Parser responsible for extracting structured information
    from a hardware specification document.
    """

    def parse(self, text: str) -> SpecificationModel:
        """
        Main parser entry point.
        """

        spec = SpecificationModel()

        spec.module_name = self._parse_module_name(text)
        spec.inputs = self._parse_inputs(text)
        spec.outputs = self._parse_outputs(text)
        spec.requirements = self._parse_requirements(text)

        return spec

    # -----------------------------------------------------
    # Module Name
    # -----------------------------------------------------

    def _parse_module_name(self, text: str) -> str:

        match = re.search(
            r"Module Name:\s*(\w+)",
            text
        )

        return match.group(1) if match else ""

    # -----------------------------------------------------
    # Inputs
    # -----------------------------------------------------

    def _parse_inputs(self, text: str) -> list[str]:

        section = re.search(
            r"Inputs:(.*?)Output:",
            text,
            re.DOTALL
        )

        if not section:
            return []

        return re.findall(
            r"-\s*(\w+)\s*:",
            section.group(1)
        )

    # -----------------------------------------------------
    # Outputs
    # -----------------------------------------------------

    def _parse_outputs(self, text: str) -> list[str]:

        section = re.search(
            r"Output:(.*?)Functional Requirements:",
            text,
            re.DOTALL
        )

        if not section:
            return []

        return re.findall(
            r"-\s*(\w+)\s*:",
            section.group(1)
        )

    # -----------------------------------------------------
    # Functional Requirements
    # -----------------------------------------------------

    def _parse_requirements(self, text: str) -> list[RequirementRule]:

        rules = []

        pattern = (
            r"If\s+(\w+)\s*=\s*(\d+),\s*"
            r"output\s+(\w+)\s+shall\s+be\s+equal\s+to\s+input\s+(\w+)"
        )

        matches = re.findall(
            pattern,
            text,
            re.IGNORECASE
        )

        for signal, value, output, expected in matches:

            rule = RequirementRule(
                condition=f"{signal} == {value}",
                output_signal=output,
                expected_value=expected
            )

            rules.append(rule)

        return rules