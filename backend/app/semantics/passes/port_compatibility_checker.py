"""
Port Compatibility Checker.

Checks whether connected ports exist.
"""


class PortCompatibilityChecker:

    def check(
        self,
        instance_ports,
        module_ports,
    ):

        diagnostics = []

        valid_ports = {
            p.name
            for p in module_ports
        }

        for connection in instance_ports:

            if connection.port_name not in valid_ports:

                diagnostics.append(
                    {
                        "kind": "UnknownPort",
                        "port": connection.port_name,
                    }
                )

        return diagnostics
