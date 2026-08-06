"""
Width inference pass.

Computes effective bit widths of signals.
"""

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
            # packed_range support comes next
            #
            if tree.packed_range is not None:
                width = None

            model.types.setdefault(
                tree.name,
                {},
            )

            model.types[tree.name]["width"] = width
