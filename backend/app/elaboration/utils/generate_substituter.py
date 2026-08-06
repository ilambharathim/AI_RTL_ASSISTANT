"""
Generate variable substitution.

Replaces occurrences of the generate variable
inside cloned AST nodes.
"""

from app.ast.expression import IdentifierExpression, LiteralExpression


class GenerateSubstituter:

    @staticmethod
    def substitute(
        node,
        variable,
        value,
    ):

        GenerateSubstituter._visit(
            node,
            variable,
            value,
        )

        return node

    @staticmethod
    def _visit(
        node,
        variable,
        value,
    ):

        if node is None:
            return

        #
        # Identifier → literal
        #
        if isinstance(
            node,
            IdentifierExpression,
        ):

            if node.name == variable:

                object.__setattr__(
                    node,
                    "name",
                    str(value),
                )

                object.__setattr__(
                    node,
                    "kind",
                    "LiteralExpression",
                )

                return

        #
        # Walk children
        #
        for attribute in dir(node):

            if attribute.startswith("_"):
                continue

            try:
                member = getattr(
                    node,
                    attribute,
                )
            except Exception:
                continue

            if isinstance(
                member,
                tuple,
            ):

                for item in member:

                    if hasattr(
                        item,
                        "__dict__",
                    ) or hasattr(
                        item,
                        "__slots__",
                    ):

                        GenerateSubstituter._visit(
                            item,
                            variable,
                            value,
                        )

            elif hasattr(
                member,
                "__dict__",
            ) or hasattr(
                member,
                "__slots__",
            ):

                GenerateSubstituter._visit(
                    member,
                    variable,
                    value,
                )

