"""
Repair Multiple Driver diagnostics.
"""

import re

from app.repair.base.repair_rule import RepairRule
from app.repair.repair_suggestion import RepairSuggestion


class MultipleDriverRepair(RepairRule):

    code = "RIVA2001"

    def repair(
        self,
        diagnostic,
        semantic_model,
    ):

        match = re.search(
            r"Signal '([^']+)'",
            diagnostic.message,
        )

        if match is None:
            return None

        signal = match.group(1)

        return RepairSuggestion(

            diagnostic_code=self.code,

            title="Resolve multiple drivers",

            explanation=(
                f"Signal '{signal}' is driven from more than one location."
            ),

            replacement=(
                f"""\
Choose ONE driver for '{signal}'.

Example:

always_comb begin
    {signal} = ...;
end

Remove every other assignment driving '{signal}'.
"""
            ),

            reason=(
                "Multiple procedural or continuous assignments detected."
            ),

        )
