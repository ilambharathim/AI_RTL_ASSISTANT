"""
Port validator.

Checks:

- Unknown ports
- Duplicate ports
- Missing ports
- Width compatibility

Canonical semantic types are preferred for width resolution,
while SymbolInfo.width remains a compatibility fallback.
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

                    signal_width = self._lookup_width(
                        expression.name,
                        semantic_model,
                    )

                    port_width = self._lookup_width(
                        connection.port_name,
                        semantic_model,
                    )

                    if (
                        signal_width is None
                        or port_width is None
                    ):
                        continue

                    if signal_width != port_width:

                        diagnostics.append(
                            f"Width mismatch on port "
                            f"'{connection.port_name}' "
                            f"in instance "
                            f"'{member.instance_name}': "
                            f"expected "
                            f"{port_width}, "
                            f"got "
                            f"{signal_width}."
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

    def _lookup_width(
        self,
        name,
        semantic_model,
    ):
        """
        Resolve width from canonical semantic types first.

        Resolution order:

            semantic_types
                ↓
            symbols
                ↓
            legacy types
        """

        #
        # Canonical semantic type repository.
        #
        semantic_types = getattr(
            semantic_model,
            "semantic_types",
            {},
        )

        semantic_type = semantic_types.get(
            name,
        )

        if semantic_type is not None:

            width = getattr(
                semantic_type,
                "width",
                None,
            )

            if width is not None:
                return width

        #
        # Symbol compatibility fallback.
        #
        symbols = getattr(
            semantic_model,
            "symbols",
            {},
        )

        symbol = symbols.get(
            name,
        )

        if symbol is not None:

            width = getattr(
                symbol,
                "width",
                None,
            )

            if width is not None:
                return width

            #
            # SymbolInfo may itself carry the canonical
            # semantic type.
            #
            symbol_type = getattr(
                symbol,
                "semantic_type",
                None,
            )

            if symbol_type is not None:

                width = getattr(
                    symbol_type,
                    "width",
                    None,
                )

                if width is not None:
                    return width

        #
        # Legacy type compatibility fallback.
        #
        types = getattr(
            semantic_model,
            "types",
            {},
        )

        type_info = types.get(
            name,
        )

        if type_info is not None:

            if isinstance(
                type_info,
                dict,
            ):
                return type_info.get(
                    "width",
                )

            return getattr(
                type_info,
                "width",
                None,
            )

        return None
