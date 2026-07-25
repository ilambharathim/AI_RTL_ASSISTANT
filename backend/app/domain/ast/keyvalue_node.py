"""
Key Value Node
"""

from dataclasses import dataclass

from app.domain.ast.ast_node import ASTNode


@dataclass
class KeyValueNode(ASTNode):

    key: str = ""
    value: str = ""

    def __init__(self, key: str, value: str):
        super().__init__(node_type="KEY_VALUE")
        self.key = key
        self.value = value
