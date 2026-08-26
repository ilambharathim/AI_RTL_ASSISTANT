"""
Signedness Resolver.

Determines signed/unsigned information for declared symbols.

The canonical SemanticModel.semantic_types repository is updated
alongside the legacy model.types representation.
"""

from app.ast import (
    CompilationUnit,
    ModuleDeclaration,
    SignalDeclaration,
)

from app.semantics.types.rtl.rtl_type import RTLType


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

            signed = (
                "signed"
                in str(tree.signal_type).lower()
            )

            #
            # Keep legacy metadata synchronized.
            #
            model.types.setdefault(
                tree.name,
                {},
            )

            model.types[
                tree.name
            ]["signed"] = signed

            #
            # Synchronize canonical semantic type.
            #
            current = model.get_semantic_type(
                tree.name,
            )

            if current is not None:

                model.set_semantic_type(
                    tree.name,
                    RTLType(
                        name=current.name,
                        width=current.width,
                        signed=signed,
                        packed=current.packed,
                    ),
                )
