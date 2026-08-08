"""
Signedness Resolver.

Determines signed/unsigned information for declared symbols.
"""

from app.ast import (
    CompilationUnit,
    ModuleDeclaration,
    SignalDeclaration,
)


class SignednessResolver:

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

            model.types.setdefault(
                tree.name,
                {},
            )

            model.types[
                tree.name
            ]["signed"] = (
                "signed" in tree.signal_type.lower()
            )
