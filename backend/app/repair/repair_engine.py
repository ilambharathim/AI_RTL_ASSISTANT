"""
Repair Engine.
"""

from app.repair.rules.undefined_identifier import (
    UndefinedIdentifierRepair,
)

from app.repair.rules.width_mismatch import (
    WidthMismatchRepair,
)

from app.repair.rules.multiple_driver import (
    MultipleDriverRepair,
)

from app.repair.confidence_evaluator import (
    ConfidenceEvaluator,
)


class RepairEngine:

    def __init__(self):

        self.rules = {

            "RIVA1001": UndefinedIdentifierRepair(),

            "RIVA2001": MultipleDriverRepair(),

            "RIVA3001": WidthMismatchRepair(),

        }

        self.confidence = (

            ConfidenceEvaluator()

        )

    def generate(

        self,

        semantic_model,

    ):

        repairs = []

        diagnostics = getattr(

            semantic_model,

            "diagnostics",

            [],

        )

        for diagnostic in diagnostics:

            rule = self.rules.get(

                diagnostic.code,

            )

            if rule is None:

                continue

            suggestion = rule.repair(

                diagnostic,

                semantic_model,

            )

            if suggestion is None:

                continue

            suggestion = self.confidence.evaluate(

                suggestion,

            )

            repairs.append(

                suggestion,

            )

        semantic_model.repairs = repairs

        return repairs
