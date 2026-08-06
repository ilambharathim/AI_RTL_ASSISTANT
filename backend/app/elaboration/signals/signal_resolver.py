"""
Signal Resolver.
"""

from app.ast import (
    SignalDeclaration,
)


class SignalResolver:

    def resolve(
        self,
        semantic_model,
    ):

        elaboration = semantic_model.elaboration

        for resolved_module in (
            elaboration.elaborated_modules.values()
        ):

            declaration = resolved_module.declaration

            resolved_module.signals.clear()

            for member in declaration.members:

                if isinstance(
                    member,
                    SignalDeclaration,
                ):

                    resolved_module.signals[
                        member.name
                    ] = member
