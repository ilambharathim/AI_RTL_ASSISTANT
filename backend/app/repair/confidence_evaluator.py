"""
Repair Confidence Evaluator.
"""


class ConfidenceEvaluator:

    def evaluate(

        self,

        suggestion,

    ):

        confidence = 50

        #
        # Exact replacement available
        #
        if suggestion.replacement:

            confidence += 20

        #
        # Width inferred
        #
        if "width" in suggestion.reason.lower():

            confidence += 20

        #
        # Declaration inference
        #
        if "declared" in suggestion.reason.lower():

            confidence += 10

        confidence = min(

            confidence,

            100,

        )

        suggestion.confidence = confidence

        suggestion.auto_apply = (

            confidence >= 90

        )

        return suggestion
