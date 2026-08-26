"""
Base Typed IR node.
Every IR object derives from IRNode.
"""


class IRNode:

    kind: str = "IRNode"
    ast = None
    semantic_type = None
    width = None
    constant = None
    location = None

    def __init__(self, kind: str = "IRNode"):
        self.kind = kind
