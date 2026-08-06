"""
Base AST visitor for semantic passes.
"""


class ASTVisitor:
    """
    Base class for all semantic visitors.

    Future visitors override visit_<NodeType>()
    methods as needed.
    """

    def visit(
        self,
        node,
    ):

        if node is None:
            return

        method_name = f"visit_{type(node).__name__}"

        visitor = getattr(
            self,
            method_name,
            self.generic_visit,
        )

        return visitor(node)

    def generic_visit(
        self,
        node,
    ):
        """
        Default implementation.

        Subclasses override node-specific handlers.
        """
        return
