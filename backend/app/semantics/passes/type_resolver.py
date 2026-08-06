"""
Semantic Type Resolver.
"""

from app.ast import (
    CompilationUnit,
    ModuleDeclaration,
    SignalDeclaration,
    ParameterDeclaration,
)


class TypeResolver:

    def resolve(
        self,
        tree,
        model,
    ):

        if isinstance(tree, CompilationUnit):
            for declaration in tree.declarations:
                self.resolve(
                    declaration,
                    model,
                )
            return

        if isinstance(tree, ModuleDeclaration):
            for member in tree.members:
                self.resolve(
                    member,
                    model,
                )
            return

        if isinstance(tree, SignalDeclaration):
            model.types[tree.name] = {
                "type": tree.signal_type,
                "packed_range": tree.packed_range,
            }
            return

        if isinstance(tree, ParameterDeclaration):
            model.types[tree.name] = {
                "type": "parameter",
            }
            return
