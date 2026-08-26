"""
RIVA Semantic Type Resolver.

Resolves RTL declarations into canonical semantic RTLType objects.

The legacy model.types dictionary is also populated for backward
compatibility with existing diagnostics and passes.
"""

from app.ast import (
    CompilationUnit,
    ModuleDeclaration,
    SignalDeclaration,
    ParameterDeclaration,
)

from app.ast.port_declaration import PortDeclaration

from app.semantics.types.rtl.rtl_type import RTLType



class TypeResolver:

    def resolve(
        self,
        syntax_tree,
        semantic_model,
    ):
        self._visit(
            syntax_tree,
            semantic_model,
        )

    def _visit(
        self,
        node,
        semantic_model,
    ):
        #
        # Compilation unit
        #
        if isinstance(
            node,
            CompilationUnit,
        ):
            for declaration in node.declarations:
                self._visit(
                    declaration,
                    semantic_model,
                )

            return

        #
        # Module
        #
        if isinstance(
            node,
            ModuleDeclaration,
        ):
            #
            # Visit port declarations (ANSI-style headers store ports
            # in node.ports, not node.members).
            #
            for port in getattr(node, "ports", ()):
                self._visit(
                    port,
                    semantic_model,
                )

            for member in node.members:
                self._visit(
                    member,
                    semantic_model,
                )

            return

        #
        # Signal declaration
        #
        if isinstance(
            node,
            SignalDeclaration,
        ):
            self._resolve_signal(
                node,
                semantic_model,
            )

            return

        #
        # Port declaration (has the same interface as SignalDeclaration).
        #
        if isinstance(
            node,
            PortDeclaration,
        ):
            self._resolve_signal(
                node,
                semantic_model,
            )

            return

        #
        # Parameter declaration
        #
        if isinstance(
            node,
            ParameterDeclaration,
        ):
            self._resolve_parameter(
                node,
                semantic_model,
            )

            return

    def _resolve_signal(
        self,
        declaration,
        semantic_model,
    ):
        width = self._infer_width(
            declaration,
        )

        signed = self._infer_signedness(
            declaration.signal_type,
        )

        packed = (
            declaration.packed_range is not None
        )

        semantic_type = RTLType(
            name=declaration.signal_type,
            width=width,
            signed=signed,
            packed=packed,
        )

        #
        # Canonical representation.
        #
        semantic_model.set_semantic_type(
            declaration.name,
            semantic_type,
        )

        #
        # Legacy representation.
        #
        semantic_model.types[
            declaration.name
        ] = {
            "type": declaration.signal_type,
            "packed_range": declaration.packed_range,
            "width": width,
            "signed": signed,
            "packed": packed,
        }

    def _resolve_parameter(
        self,
        declaration,
        semantic_model,
    ):
        #
        # Parameters do not currently have a dedicated
        # parameter semantic type. Keep their existing
        # representation stable.
        #
        semantic_model.types[
            declaration.name
        ] = {
            "type": "parameter",
        }

    def _infer_width(
        self,
        declaration,
    ):
        packed_range = declaration.packed_range

        if packed_range is None:
            return 1

        left = getattr(
            packed_range,
            "left",
            None,
        )

        right = getattr(
            packed_range,
            "right",
            None,
        )

        left_value = self._evaluate_bound(
            left,
        )

        right_value = self._evaluate_bound(
            right,
        )

        if left_value is None or right_value is None:
            return 1

        return abs(
            left_value - right_value
        ) + 1

    def _evaluate_bound(
        self,
        expression,
    ):
        if expression is None:
            return None

        #
        # LiteralExpression currently stores its
        # textual value in .value.
        #
        value = getattr(
            expression,
            "value",
            None,
        )

        if value is not None:
            try:
                return int(
                    str(value),
                    0,
                )
            except ValueError:
                try:
                    return int(
                        str(value),
                    )
                except ValueError:
                    return None

        return None

    def _infer_signedness(
        self,
        signal_type,
    ):
        text = str(
            signal_type
        ).lower()

        return "signed" in text
