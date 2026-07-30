"""
Identifier resolution visitor.
"""

from app.ast import (
    ProceduralAssignment,
)

class IdentifierResolver:

    def __init__(self):

        self.errors = []

    def visit(
        self,
        scope,
        node,
    ):

        #
        # Assignment
        #
        if isinstance(
            node,
            ProceduralAssignment,
        ):

            #
            # Resolve target
            #
            if scope.lookup(node.target) is None:

                self.errors.append(
                    f"Undefined identifier '{node.target}'"
                )

            #
            # Resolve simple identifier expressions
            #
            expression = node.expression.strip()

            if expression.isidentifier():

                if scope.lookup(expression) is None:

                    self.errors.append(
                        f"Undefined identifier '{expression}'"
                    )
