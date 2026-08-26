"""
Adapter from the legacy RTL AST to the new domain RTL AST.

The parser continues to produce the legacy AST while this adapter
provides the migration boundary into the new RTL domain AST.
"""

from app.ast.always_block import AlwaysBlock
from app.ast.compilation_unit import CompilationUnit
from app.ast.continuous_assign import ContinuousAssign
from app.ast.generate_block import GenerateBlock
from app.ast.generate_for import GenerateFor
from app.ast.generate_if import GenerateIf
from app.ast.module_declaration import ModuleDeclaration
from app.ast.module_instance import ModuleInstance
from app.ast.parameter_declaration import ParameterDeclaration
from app.ast.port_declaration import PortDeclaration
from app.ast.signal_declaration import SignalDeclaration

from app.domain.rtl_ast import (
    AssignNode,
    GenerateNode,
    InstanceNode,
    ModuleNode,
    ParameterNode,
    PortNode,
    RTLCompilationUnit,
    SignalNode,
    AlwaysBlockNode,
)


class LegacyToRTLASTAdapter:
    """
    Convert legacy parser AST nodes into the new RTL domain AST.
    """

    @staticmethod
    def convert(
        syntax_tree,
    ) -> RTLCompilationUnit:
        """
        Convert a legacy CompilationUnit into RTLCompilationUnit.
        """

        if not isinstance(syntax_tree, CompilationUnit):
            raise TypeError(
                "syntax_tree must be a legacy CompilationUnit."
            )

        result = RTLCompilationUnit()

        for declaration in syntax_tree.declarations:
            if isinstance(declaration, ModuleDeclaration):
                result.add_module(
                    LegacyToRTLASTAdapter._convert_module(
                        declaration
                    )
                )

        return result

    @staticmethod
    def _convert_module(
        declaration: ModuleDeclaration,
    ) -> ModuleNode:
        """
        Convert one legacy ModuleDeclaration.
        """

        module = ModuleNode(
            name=declaration.name,
        )

        for port in declaration.ports:
            if isinstance(port, PortDeclaration):
                module.add_port(
                    LegacyToRTLASTAdapter._convert_port(
                        port
                    )
                )

        for member in declaration.members:
            if isinstance(member, ParameterDeclaration):
                module.add_parameter(
                    LegacyToRTLASTAdapter._convert_parameter(
                        member
                    )
                )
                continue

            converted = (
                LegacyToRTLASTAdapter._convert_member(
                    member
                )
            )

            if converted is not None:
                module.add_member(converted)

        return module

    @staticmethod
    def _convert_port(
        declaration: PortDeclaration,
    ) -> PortNode:
        """
        Convert one legacy PortDeclaration.
        """

        return PortNode(
            name=declaration.name,
            direction=declaration.direction,
            datatype=declaration.signal_type,
            width=(
                LegacyToRTLASTAdapter._packed_range_width(
                    declaration.packed_range
                )
                if declaration.packed_range is not None
                else 1
            ),
        )

    @staticmethod
    def _convert_parameter(
        declaration: ParameterDeclaration,
    ) -> ParameterNode:
        """
        Convert one legacy ParameterDeclaration.
        """

        return ParameterNode(
            name=declaration.name,
            value=LegacyToRTLASTAdapter._expression_text(
                declaration.value
            ),
        )

    @staticmethod
    def _convert_member(
        declaration,
    ):
        """
        Convert supported legacy module members.
        """

        if isinstance(declaration, SignalDeclaration):
            return SignalNode(
                name=declaration.name,
                datatype=declaration.signal_type,
                width=(
                    LegacyToRTLASTAdapter._packed_range_width(
                        declaration.packed_range
                    )
                    if declaration.packed_range is not None
                    else 1
                ),
            )

        if isinstance(declaration, ContinuousAssign):
            return AssignNode(
                target=declaration.target,
                expression=declaration.expression,
            )

        if isinstance(declaration, ModuleInstance):
            return LegacyToRTLASTAdapter._convert_instance(
                declaration
            )

        if isinstance(declaration, AlwaysBlock):
            return LegacyToRTLASTAdapter._convert_always(
                declaration
            )

        if isinstance(declaration, GenerateBlock):
            return GenerateNode(
                generate_type="block",
            )

        if isinstance(declaration, GenerateFor):
            return GenerateNode(
                condition=LegacyToRTLASTAdapter._expression_text(
                    declaration.condition
                ),
                generate_type="for",
            )

        if isinstance(declaration, GenerateIf):
            return GenerateNode(
                condition=LegacyToRTLASTAdapter._expression_text(
                    declaration.condition
                ),
                generate_type="if",
            )

        return None

    @staticmethod
    def _convert_instance(
        declaration: ModuleInstance,
    ) -> InstanceNode:
        """
        Convert one legacy ModuleInstance.
        """

        return InstanceNode(
            module_name=declaration.module_name,
            instance_name=declaration.instance_name,
            parameter_overrides=list(
                declaration.parameter_overrides
            ),
            connections=list(
                declaration.connections
            ),
        )

    @staticmethod
    def _convert_always(
        declaration: AlwaysBlock,
    ) -> AlwaysBlockNode:
        """
        Convert one legacy AlwaysBlock.
        """

        return AlwaysBlockNode(
            block_type=declaration.block_type,
            sensitivity=declaration.sensitivity,
            statements=list(declaration.statements),
        )

    @staticmethod
    def _expression_text(
        node,
    ) -> str:
        """
        Convert a legacy expression node into stable text.

        The new AST currently stores expressions as strings, while
        the legacy AST may represent them as expression nodes.
        """

        if node is None:
            return ""

        if isinstance(node, str):
            return node

        value = getattr(node, "value", None)
        if value is not None:
            return str(value)

        name = getattr(node, "name", None)
        if name is not None:
            return str(name)

        operator = getattr(node, "operator", None)

        if operator is not None:
            left = getattr(node, "left", None)
            right = getattr(node, "right", None)

            if left is not None and right is not None:
                return (
                    f"{LegacyToRTLASTAdapter._expression_text(left)} "
                    f"{operator} "
                    f"{LegacyToRTLASTAdapter._expression_text(right)}"
                )

            operand = getattr(node, "operand", None)
            if operand is not None:
                return (
                    f"{operator}"
                    f"{LegacyToRTLASTAdapter._expression_text(operand)}"
                )

        function_name = getattr(
            node,
            "function_name",
            None,
        )

        if function_name is not None:
            arguments = getattr(
                node,
                "arguments",
                (),
            )

            rendered = ", ".join(
                LegacyToRTLASTAdapter._expression_text(
                    argument
                )
                for argument in arguments
            )

            return f"{function_name}({rendered})"

        return str(node)

    @staticmethod
    def _packed_range_width(
        packed_range,
    ) -> int:
        """
        Extract width from a legacy packed-range AST.
        """

        if packed_range is None:
            return 1

        left_value = LegacyToRTLASTAdapter._literal_int(
            getattr(packed_range, "left", None)
        )

        right_value = LegacyToRTLASTAdapter._literal_int(
            getattr(packed_range, "right", None)
        )

        if (
            left_value is not None
            and right_value is not None
        ):
            return abs(left_value - right_value) + 1

        return 1

    @staticmethod
    def _literal_int(
        node,
    ) -> int | None:
        """
        Extract an integer from a legacy literal-expression node.
        """

        if isinstance(node, int):
            return node

        value = getattr(node, "value", None)

        if isinstance(value, int):
            return value

        if isinstance(value, str):
            try:
                return int(value, 0)
            except ValueError:
                return None

        return None
