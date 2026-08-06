"""
Context-aware Undefined Identifier Repair.
"""

import re

from app.repair.base.repair_rule import RepairRule
from app.repair.repair_suggestion import RepairSuggestion


class UndefinedIdentifierRepair(RepairRule):

    code = "RIVA1001"

    def repair(
        self,
        diagnostic,
        semantic_model,
    ):

        match = re.search(
            r"'([^']+)'",
            diagnostic.message,
        )

        if match is None:
            return None

        name = match.group(1)

        width = 1

        #
        # Infer width from existing symbols.
        #
        for symbol in semantic_model.symbols.values():

            if symbol.width is not None:

                width = max(
                    width,
                    symbol.width,
                )

        if width == 1:

            declaration = f"logic {name};"

        else:

            declaration = (
                f"logic [{width-1}:0] {name};"
            )

        return RepairSuggestion(

            diagnostic_code=self.code,

            title="Declare missing signal",

            explanation=(
                f"'{name}' is referenced but not declared."
            ),

            replacement=declaration,

            reason=(
                "Width inferred from existing declarations."
            ),

        )
