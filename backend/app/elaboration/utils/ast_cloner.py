"""
AST cloning utilities.

Used during elaboration.
"""

from copy import deepcopy


class ASTCloner:

    @staticmethod
    def clone(node):

        return deepcopy(node)

