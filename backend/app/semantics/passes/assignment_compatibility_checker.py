"""
Assignment Compatibility Checker.

Checks width compatibility between procedural assignments.

Destination type resolution prefers the canonical
SemanticModel.semantic_types repository, while retaining
symbols and legacy types as compatibility fallbacks.
"""

from app.ast import (
    CompilationUnit,
    ModuleDeclaration,
    ProceduralAssignment,
)

from app.diagnostics.diagnostic import Diagnostic
from app.diagnostics.catalog.width_catalog import RIVA3001

from app.semantics.passes.expression_type_checker import (
    ExpressionTypeChecker,
)


class AssignmentCompatibilityChecker:

    def __init__(self):

        self.expression_type_checker = (
            ExpressionTypeChecker()
        )

    def check(
        self,
        tree,
        model,
    ):

        if isinstance(
            tree,
            CompilationUnit,
        ):

            for declaration in tree.declarations:

                self.check(
                    declaration,
                    model,
                )

            return

        if isinstance(
            tree,
            ModuleDeclaration,
        ):

            for member in tree.members:

                self.check(
                    member,
                    model,
                )

            return

        if isinstance(
            tree,
            ProceduralAssignment,
        ):

            self._check_assignment(
                tree,
                model,
            )

    def _lookup_target_type(
        self,
        target_name,
        model,
    ):
        """
        Resolve destination type using canonical semantic types first.

        Resolution order:

            semantic_types
                ↓
            symbols
                ↓
            legacy types
        """

        semantic_types = getattr(
            model,
            "semantic_types",
            {},
        )

        target_info = semantic_types.get(
            target_name,
        )

        if target_info is not None:
            return target_info

        symbols = getattr(
            model,
            "symbols",
            {},
        )

        target_info = symbols.get(
            target_name,
        )

        if target_info is not None:
            return target_info

        types = getattr(
            model,
            "types",
            {},
        )

        return types.get(
            target_name,
        )

    def _get_width(
        self,
        type_info,
    ):
        """
        Extract width from either an RTLType-like object
        or the legacy dictionary representation.
        """

        if type_info is None:
            return None

        if hasattr(
            type_info,
            "width",
        ):

            return type_info.width

        if isinstance(
            type_info,
            dict,
        ):

            return type_info.get(
                "width",
            )

        return None

    def _check_assignment(
        self,
        assignment,
        model,
    ):

        lhs = assignment.target

        lhs_type = self._lookup_target_type(
            lhs,
            model,
        )

        if lhs_type is None:
            return

        lhs_width = self._get_width(
            lhs_type,
        )

        if lhs_width is None:
            return

        rhs_expression = assignment.expression

        rhs_type = self.expression_type_checker.infer(
            rhs_expression,
            model,
        )

        if rhs_type is None:
            return

        rhs_width = rhs_type.get(
            "width",
        )

        if rhs_width is None:
            return

        if lhs_width == rhs_width:
            return

        rhs_name = getattr(
            rhs_expression,
            "name",
            None,
        )

        if rhs_name is not None:

            rhs_description = (
                f"{rhs_name} ({rhs_width} bits)"
            )

        else:

            rhs_description = (
                f"{rhs_width} bits"
            )

        model.diagnostics.append(
            Diagnostic(
                code=RIVA3001.code,
                category=RIVA3001.category,
                severity=RIVA3001.severity,
                message=(
                    f"Width mismatch: "
                    f"{lhs} ({lhs_width} bits) <- "
                    f"{rhs_description}"
                ),
                explanation=RIVA3001.explanation,
                suggestion=RIVA3001.suggestion,
                location=getattr(assignment, "location", None),
            )
        )
