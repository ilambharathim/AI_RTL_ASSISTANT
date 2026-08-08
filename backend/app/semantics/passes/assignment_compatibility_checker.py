"""
Assignment Compatibility Checker.

Checks width compatibility between procedural assignments.
"""

from app.ast import (
    CompilationUnit,
    ModuleDeclaration,
    ProceduralAssignment,
)


class AssignmentCompatibilityChecker:

    def check(
        self,
        tree,
        model,
    ):

        if isinstance(tree, CompilationUnit):

            for declaration in tree.declarations:
                self.check(declaration, model)

            return

        if isinstance(tree, ModuleDeclaration):

            for member in tree.members:
                self.check(member, model)

            return

        if isinstance(tree, ProceduralAssignment):

            lhs = tree.target

            rhs = getattr(
                tree.expression,
                "name",
                None,
            )

            if rhs is None:
                return

            if lhs not in model.types:
                return

            if rhs not in model.types:
                return

            lhs_width = model.types[lhs].get("width")
            rhs_width = model.types[rhs].get("width")

            if (
                lhs_width is not None
                and rhs_width is not None
                and lhs_width != rhs_width
            ):
                model.diagnostics.append(
                    {
                        "kind": "WidthMismatch",
                        "lhs": lhs,
                        "rhs": rhs,
                        "lhs_width": lhs_width,
                        "rhs_width": rhs_width,
                    }
                )
