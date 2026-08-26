"""
Width inference pass.

Computes effective bit widths of signals and synchronizes
both the legacy type metadata and canonical RTLType objects.
"""

from app.semantics.passes.expression_evaluator import (
    ExpressionEvaluator,
)

from app.ast import (
    CompilationUnit,
    ModuleDeclaration,
    SignalDeclaration,
)

from app.semantics.types.rtl.rtl_type import RTLType


class WidthInference:

    def infer(
        self,
        tree,
        model,
    ):

        if isinstance(
            tree,
            CompilationUnit,
        ):

            for declaration in tree.declarations:

                self.infer(
                    declaration,
                    model,
                )

            return

        if isinstance(
            tree,
            ModuleDeclaration,
        ):

            for member in tree.members:

                self.infer(
                    member,
                    model,
                )

            return

        if isinstance(
            tree,
            SignalDeclaration,
        ):

            width = 1

            if tree.packed_range is not None:

                left = ExpressionEvaluator.evaluate(
                    tree.packed_range.left,
                )

                right = ExpressionEvaluator.evaluate(
                    tree.packed_range.right,
                )

                width = abs(
                    left - right
                ) + 1

            #
            # Keep legacy metadata synchronized.
            #
            model.types.setdefault(
                tree.name,
                {},
            )

            model.types[
                tree.name
            ]["width"] = width

            #
            # Synchronize canonical semantic type.
            #
            current = model.get_semantic_type(
                tree.name,
            )

            if current is not None:

                model.set_semantic_type(
                    tree.name,
                    RTLType(
                        name=current.name,
                        width=width,
                        signed=current.signed,
                        packed=current.packed,
                    ),
                )
