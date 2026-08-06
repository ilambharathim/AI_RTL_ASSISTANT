"""
Module instance AST node.
"""

from dataclasses import dataclass

from app.ast.node import ASTNode


@dataclass(frozen=True, slots=True)
class ModuleInstance(ASTNode):

    module_name: str

    parameter_overrides: tuple

    instance_name: str

    connections: tuple

    def __init__(
        self,
        module_name,
        parameter_overrides,
        instance_name,
        connections,
    ):

        object.__setattr__(
            self,
            "kind",
            "ModuleInstance",
        )

        object.__setattr__(
            self,
            "module_name",
            module_name,
        )

        object.__setattr__(
            self,
            "parameter_overrides",
            parameter_overrides,
        )

        object.__setattr__(
            self,
            "instance_name",
            instance_name,
        )

        object.__setattr__(
            self,
            "connections",
            connections,
        )


        object.__setattr__(
            self,
            "location",
            None,
        )

