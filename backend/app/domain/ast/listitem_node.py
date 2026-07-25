"""
List Item Node
"""

from dataclasses import dataclass

from app.domain.ast.ast_node import ASTNode


@dataclass
class ListItemNode(ASTNode):

    value: str = ""

    def __init__(self, value: str):
        super().__init__(node_type="LIST_ITEM")
        self.value = value
