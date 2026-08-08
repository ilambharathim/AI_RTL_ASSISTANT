"""
Constant Propagation Pass.

Propagates compile-time constant values through the semantic model.
"""

from app.ast import (
    CompilationUnit,
    ModuleDeclaration,
    ParameterDeclaration,
)

from app.semantics.passes.expression_evaluator import (
    ExpressionEvaluator,
)


class ConstantPropagation:

    def propagate(
        self,
        tree,
        model,
    ):

        if isinstance(tree, CompilationUnit):

            for declaration in tree.declarations:
                self.propagate(
                    declaration,
                    model,
                )

            return

        if isinstance(tree, ModuleDeclaration):

            for member in tree.members:
                self.propagate(
                    member,
                    model,
                )

            return

        if isinstance(tree, ParameterDeclaration):

            value = ExpressionEvaluator.evaluate(
                tree.value,
            )

            model.constant_values[
                tree.name
            ] = value
