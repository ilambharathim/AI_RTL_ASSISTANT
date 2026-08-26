"""
Signedness Mismatch Detection.

Detects assignments whose source and destination signedness differ.

Destination type resolution prefers the canonical
SemanticModel.semantic_types repository, while retaining
symbols and legacy types as compatibility fallbacks.
"""

from app.ast import (
    ContinuousAssign,
    ProceduralAssignment,
    ModuleDeclaration,
    CompilationUnit,
    AlwaysBlock,
    StatementBlock,
    IfStatement,
)

from app.diagnostics.base.diagnostic_rule import (
    DiagnosticRule,
)

from app.diagnostics.diagnostic import (
    Diagnostic,
)

from app.diagnostics.catalog.width_catalog import (
    RIVA3002,
)

from app.semantics.passes.expression_type_checker import (
    ExpressionTypeChecker,
)


class SignednessMismatchRule(DiagnosticRule):

    code = RIVA3002.code
    name = "Signedness Mismatch"

    def __init__(self):

        self.expression_type_checker = (
            ExpressionTypeChecker()
        )

    def run(
        self,
        semantic_model,
    ):

        self.semantic_model = semantic_model

        diagnostics = []

        self.diagnostics = diagnostics

        self._visit(
            semantic_model.syntax_tree,
        )

        return diagnostics

    def _visit(
        self,
        node,
    ):

        if node is None:
            return

        if isinstance(
            node,
            CompilationUnit,
        ):

            for declaration in node.declarations:

                self._visit(
                    declaration,
                )

            return

        if isinstance(
            node,
            ModuleDeclaration,
        ):

            for member in node.members:

                self._visit(
                    member,
                )

            return

        if isinstance(
            node,
            AlwaysBlock,
        ):

            for statement in node.statements:

                self._visit(
                    statement,
                )

            return

        if isinstance(
            node,
            StatementBlock,
        ):

            for statement in node.statements:

                self._visit(
                    statement,
                )

            return

        if isinstance(
            node,
            IfStatement,
        ):

            self._visit(
                node.then_branch,
            )

            self._visit(
                node.else_branch,
            )

            return

        if isinstance(
            node,
            (
                ContinuousAssign,
                ProceduralAssignment,
            ),
        ):

            self._check_assignment(
                node,
            )

    def _lookup_target_type(
        self,
        target_name,
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
            self.semantic_model,
            "semantic_types",
            {},
        )

        target_info = semantic_types.get(
            target_name,
        )

        if target_info is not None:
            return target_info

        symbols = getattr(
            self.semantic_model,
            "symbols",
            {},
        )

        target_info = symbols.get(
            target_name,
        )

        if target_info is not None:
            return target_info

        types = getattr(
            self.semantic_model,
            "types",
            {},
        )

        return types.get(
            target_name,
        )

    def _get_signedness(
        self,
        type_info,
    ):
        """
        Extract signedness from either an RTLType-like
        object or the legacy dictionary representation.
        """

        if type_info is None:
            return None

        if hasattr(
            type_info,
            "signed",
        ):

            return type_info.signed

        if isinstance(
            type_info,
            dict,
        ):

            return type_info.get(
                "signed",
            )

        return None

    def _check_assignment(
        self,
        assignment,
    ):

        target_name = assignment.target
        expression = assignment.expression

        target_info = self._lookup_target_type(
            target_name,
        )

        if target_info is None:
            return

        destination_signed = self._get_signedness(
            target_info,
        )

        if destination_signed is None:
            return

        #
        # Infer signedness from the complete RHS expression.
        #
        source_info = self.expression_type_checker.infer(
            expression,
            self.semantic_model,
        )

        if source_info is None:
            return

        source_signed = source_info.get(
            "signed",
        )

        if source_signed is None:
            return

        if destination_signed == source_signed:
            return

        source_name = getattr(
            expression,
            "name",
            None,
        )

        if source_name is not None:

            source_description = (
                f"{source_name} "
                f"({'signed' if source_signed else 'unsigned'})"
            )

        else:

            source_description = (
                f"expression "
                f"({'signed' if source_signed else 'unsigned'})"
            )

        self.diagnostics.append(
            Diagnostic(
                code=RIVA3002.code,
                category=RIVA3002.category,
                severity=RIVA3002.severity,
                message=(
                    f"Signedness mismatch: "
                    f"{target_name} "
                    f"({'signed' if destination_signed else 'unsigned'}) <- "
                    f"{source_description}"
                ),
                explanation=RIVA3002.explanation,
                suggestion=RIVA3002.suggestion,
                location=getattr(assignment, "location", None),
            )
        )

