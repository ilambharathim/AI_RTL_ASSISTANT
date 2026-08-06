"""
Hierarchy elaboration.
"""

from app.ast import (
    ModuleDeclaration,
    ModuleInstance,
)


class HierarchyElaborator:

    def elaborate(
        self,
        syntax_tree,
        semantic_model,
    ):

        hierarchy = semantic_model.elaboration.hierarchy

        hierarchy.clear()

        for declaration in syntax_tree.declarations:

            if not isinstance(
                declaration,
                ModuleDeclaration,
            ):
                continue

            hierarchy[
                declaration.name
            ] = []

            for member in declaration.members:

                if isinstance(
                    member,
                    ModuleInstance,
                ):

                    hierarchy[
                        declaration.name
                    ].append(

                        member.instance_name

                    )

