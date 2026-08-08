"""
Width inference pass.

Computes effective bit widths of signals.
"""

from app.semantics.passes.expression_evaluator import (
    ExpressionEvaluator,
)

from app.ast import (
    CompilationUnit,
    ModuleDeclaration,
    SignalDeclaration,
)


class WidthInference:

    def infer(
        self,
        tree,
        model,
    ):

        if isinstance(tree, CompilationUnit):

            for declaration in tree.declarations:
                self.infer(
                    declaration,
                    model,
                )

            return

        if isinstance(tree, ModuleDeclaration):

            for member in tree.members:
                self.infer(
                    member,
                    model,
                )

            return

        if isinstance(tree, SignalDeclaration):

            #
            # Default width
            #
            width = 1

            #
            # Packed range width
            #
            if tree.packed_range is not None:

                left = ExpressionEvaluator.evaluate(
                    tree.packed_range.left,
                )

                right = ExpressionEvaluator.evaluate(
                    tree.packed_range.right,
                )

                width = abs(left - right) + 1

            model.types.setdefault(
                tree.name,
                {},
            )

            model.types[tree.name]["width"] = width
