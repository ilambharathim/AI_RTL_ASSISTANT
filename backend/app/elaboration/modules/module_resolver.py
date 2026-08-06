"""
Module Resolver.
"""

from app.ast import (
    ModuleDeclaration,
)

from app.elaboration.model import (
    ResolvedModule,
)


class ModuleResolver:

    def resolve(
        self,
        syntax_tree,
        semantic_model,
    ):

        elaboration = semantic_model.elaboration

        elaboration.elaborated_modules.clear()

        for declaration in syntax_tree.declarations:

            if not isinstance(
                declaration,
                ModuleDeclaration,
            ):
                continue

            resolved = ResolvedModule(

                name=declaration.name,

                declaration=declaration,

            )

            elaboration.elaborated_modules[
                declaration.name
            ] = resolved
