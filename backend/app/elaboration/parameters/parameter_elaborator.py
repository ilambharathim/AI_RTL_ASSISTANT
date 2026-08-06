"""
Parameter elaboration.
"""

from app.ast import ModuleInstance


class ParameterElaborator:

    def elaborate(
        self,
        syntax_tree,
        semantic_model,
    ):

        semantic_model.elaboration.instance_parameters.clear()

        for declaration in syntax_tree.declarations:

            if not hasattr(
                declaration,
                "members",
            ):
                continue

            for member in declaration.members:

                if not isinstance(
                    member,
                    ModuleInstance,
                ):
                    continue

                resolved = {}

                for override in getattr(
                    member,
                    "parameter_overrides",
                    (),
                ):
                    resolved[
                        override.name
                    ] = override.expression

                semantic_model.elaboration.instance_parameters[
                    member.instance_name
                ] = resolved

