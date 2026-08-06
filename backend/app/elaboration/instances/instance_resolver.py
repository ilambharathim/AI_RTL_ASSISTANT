"""
Instance Resolver.

Converts ModuleInstance AST nodes into typed ResolvedInstance objects.
"""

from app.ast import ModuleInstance

from app.elaboration.model import (
    ResolvedInstance,
)


class InstanceResolver:

    def resolve(
        self,
        syntax_tree,
        semantic_model,
    ):

        elaboration = semantic_model.elaboration

        for resolved_module in (
            elaboration.elaborated_modules.values()
        ):

            declaration = resolved_module.declaration

            resolved_module.instances.clear()

            for member in declaration.members:

                if not isinstance(
                    member,
                    ModuleInstance,
                ):
                    continue

                resolved = ResolvedInstance(

                    instance_name=member.instance_name,

                    module_name=member.module_name,

                    module=elaboration.elaborated_modules.get(
                        member.module_name,
                    ),

                    connections=member.connections,

                    parameter_overrides=member.parameter_overrides,

                )

                resolved_module.instances[
                    resolved.instance_name
                ] = resolved
