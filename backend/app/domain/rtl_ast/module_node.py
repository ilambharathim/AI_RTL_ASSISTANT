from dataclasses import dataclass, field

from app.domain.rtl_ast.rtl_node import RTLNode


@dataclass(slots=True)
class ModuleNode(RTLNode):
    """
    Represents one RTL module.
    """

    name: str = ""

    ports: list[RTLNode] = field(
        default_factory=list,
    )

    parameters: list[RTLNode] = field(
        default_factory=list,
    )

    members: list[RTLNode] = field(
        default_factory=list,
    )

    def add_port(
        self,
        port: RTLNode,
    ) -> None:
        if not isinstance(port, RTLNode):
            raise TypeError(
                "port must be an RTLNode."
            )

        self.ports.append(port)
        self.add_child(port)

    def add_parameter(
        self,
        parameter: RTLNode,
    ) -> None:
        if not isinstance(parameter, RTLNode):
            raise TypeError(
                "parameter must be an RTLNode."
            )

        self.parameters.append(parameter)
        self.add_child(parameter)

    def add_member(
        self,
        member: RTLNode,
    ) -> None:
        if not isinstance(member, RTLNode):
            raise TypeError(
                "member must be an RTLNode."
            )

        self.members.append(member)
        self.add_child(member)
