"""
RTL elaboration.

Builds module hierarchy.
"""

from app.ast import (
    ModuleDeclaration,
)

from app.ast.module_instance import (
    ModuleInstance,
)

from app.elaboration.hierarchy_node import (
    HierarchyNode,
)


class ModuleElaborator:

    def elaborate(
        self,
        syntax_tree,
    ):

        #
        # Collect every module.
        #
        modules = {}

        for declaration in syntax_tree.declarations:

            if isinstance(
                declaration,
                ModuleDeclaration,
            ):

                modules[
                    declaration.name
                ] = declaration

        #
        # Build hierarchy roots.
        #
        hierarchy = {}

        for module in modules.values():

            hierarchy[
                module.name
            ] = self._build(
                module,
                modules,
            )

        return hierarchy

    def _build(
        self,
        module,
        modules,
    ):

        node = HierarchyNode(

            name=module.name,

            module_name=module.name,

        )

        for member in module.members:

            if isinstance(
                member,
                ModuleInstance,
            ):

                child = HierarchyNode(

                    name=member.instance_name,

                    module_name=member.module_name,

                )

                #
                # recurse if module exists
                #
                if member.module_name in modules:

                    built = self._build(

                        modules[
                            member.module_name
                        ],

                        modules,

                    )

                    child.children = built.children

                node.children.append(
                    child,
                )

        return node

