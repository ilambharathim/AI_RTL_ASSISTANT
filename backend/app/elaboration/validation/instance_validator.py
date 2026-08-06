"""
Module instance validator.

Checks that instantiated modules exist.
"""

from app.ast import ModuleDeclaration
from app.ast.module_instance import ModuleInstance


class InstanceValidator:

    def validate(
        self,
        syntax_tree,
    ):

        diagnostics = []

        modules = set()

        #
        # Collect declared modules
        #
        for declaration in syntax_tree.declarations:

            if isinstance(
                declaration,
                ModuleDeclaration,
            ):

                modules.add(
                    declaration.name,
                )

        #
        # Validate every instance
        #
        for declaration in syntax_tree.declarations:

            if not isinstance(
                declaration,
                ModuleDeclaration,
            ):
                continue

            for member in declaration.members:

                if not isinstance(
                    member,
                    ModuleInstance,
                ):
                    continue

                if member.module_name not in modules:

                    diagnostics.append(

                        f"Unknown module '{member.module_name}' "

                        f"instantiated as '{member.instance_name}'."

                    )

        return diagnostics

