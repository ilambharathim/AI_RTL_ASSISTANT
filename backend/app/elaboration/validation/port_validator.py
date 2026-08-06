"""
Port validator.

Checks:

- Unknown ports
- Duplicate ports
- Missing ports
- Width compatibility
"""

from app.ast import (
    ModuleDeclaration,
    SignalDeclaration,
)

from app.ast.module_instance import ModuleInstance


class PortValidator:

    def validate(
        self,
        syntax_tree,
        semantic_model,
    ):

        diagnostics = []

        modules = {}

        #
        # Collect modules
        #
        for declaration in syntax_tree.declarations:

            if isinstance(
                declaration,
                ModuleDeclaration,
            ):

                modules[
                    declaration.name
                ] = declaration

        #
        # Validate every module
        #
        for declaration in syntax_tree.declarations:

            if not isinstance(
                declaration,
                ModuleDeclaration,
            ):
                continue

            #
            # Local symbol widths
            #
            local_widths = {}

            for member in declaration.members:

                if isinstance(
                    member,
                    SignalDeclaration,
                ):

                    symbol = semantic_model.symbols.get(
                        member.name,
                    )

                    if symbol is not None:

                        local_widths[
                            member.name
                        ] = symbol.width

            #
            # Validate module instances
            #
            for member in declaration.members:

                if not isinstance(
                    member,
                    ModuleInstance,
                ):
                    continue

                target = modules.get(
                    member.module_name,
                )

                if target is None:
                    continue

                declared_ports = {
                    port.name: port
                    for port in target.ports
                }

                connected = set()

                for connection in member.connections:

                    #
                    # Duplicate connection
                    #
                    if connection.port_name in connected:

                        diagnostics.append(

                            f"Duplicate connection to port "
                            f"'{connection.port_name}' "
                            f"in instance "
                            f"'{member.instance_name}'."

                        )

                    connected.add(
                        connection.port_name,
                    )

                    #
                    # Unknown port
                    #
                    if connection.port_name not in declared_ports:

                        diagnostics.append(

                            f"Unknown port "
                            f"'{connection.port_name}' "
                            f"for module "
                            f"'{member.module_name}'."

                        )

                        continue

                    #
                    # Width check
                    #
                    expression = connection.expression

                    if not hasattr(
                        expression,
                        "name",
                    ):
                        continue

                    signal_symbol = semantic_model.symbols.get(
                        expression.name,
                    )

                    port_symbol = semantic_model.symbols.get(
                        connection.port_name,
                    )

                    if (
                        signal_symbol is None
                        or port_symbol is None
                    ):
                        continue

                    if (
                        signal_symbol.width is not None
                        and port_symbol.width is not None
                        and signal_symbol.width != port_symbol.width
                    ):

                        diagnostics.append(

                            f"Width mismatch on port "
                            f"'{connection.port_name}' "
                            f"in instance "
                            f"'{member.instance_name}': "

                            f"expected "
                            f"{port_symbol.width}, "

                            f"got "
                            f"{signal_symbol.width}."

                        )

                #
                # Missing ports
                #
                for port_name in declared_ports:

                    if port_name not in connected:

                        diagnostics.append(

                            f"Missing connection for port "
                            f"'{port_name}' "
                            f"in instance "
                            f"'{member.instance_name}'."

                        )

        return diagnostics

