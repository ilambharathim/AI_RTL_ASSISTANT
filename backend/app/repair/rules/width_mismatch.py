"""
Repair width mismatches.
"""

import re

from app.repair.base.repair_rule import RepairRule
from app.repair.repair_suggestion import RepairSuggestion


class WidthMismatchRepair(RepairRule):

    code = "RIVA3001"

    def repair(
        self,
        diagnostic,
        semantic_model,
    ):

        message = diagnostic.message

        match = re.search(
            r"Width mismatch:\s+(\w+)\s+\((\d+)\s+bits\)\s+<-\s+(\w+)\s+\((\d+)\s+bits\)",
            message,
        )

        if match is None:
            return None

        destination = match.group(1)

        destination_width = int(match.group(2))

        source = match.group(3)

        source_width = int(match.group(4))

        if source_width > destination_width:

            replacement = (
                f"assign {destination} = "
                f"{source}[{destination_width-1}:0];"
            )

            explanation = (
                "The source signal is wider than the destination. "
                "Truncate the upper bits."
            )

        else:

            extension = (
                destination_width
                - source_width
            )

            replacement = (
                f"assign {destination} = "
                f"{{{extension}'b0, {source}}};"
            )

            explanation = (
                "The source signal is narrower than the destination. "
                "Zero-extend the source."
            )

        return RepairSuggestion(

            diagnostic_code=self.code,

            title="Repair width mismatch",

            explanation=explanation,

            replacement=replacement,

            reason=(
                "Width inferred from source and destination signals."
            ),

        )
