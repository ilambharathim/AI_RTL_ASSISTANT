"""
Type resolution pass.

Assigns semantic types to declarations.
"""

from app.ast import (
    SignalDeclaration,
    ParameterDeclaration,
)


class TypeResolver:

    def resolve(
        self,
        syntax_tree,
        semantic_model,
    ):

        for declaration in syntax_tree.declarations:

            self._visit(
                declaration,
                semantic_model,
            )

    def _visit(
        self,
        node,
        semantic_model,
    ):

        #
        # Recurse into modules
        #
        if hasattr(
            node,
            "members",
        ):

            for member in node.members:

                self._visit(
                    member,
                    semantic_model,
                )

            return

        #
        # Signal
        #
        if isinstance(
            node,
            SignalDeclaration,
        ):

            semantic_model.types[
                node.name
            ] = node.signal_type

        #
        # Parameter
        #
        elif isinstance(
            node,
            ParameterDeclaration,
        ):

            semantic_model.types[
                node.name
            ] = "parameter"
