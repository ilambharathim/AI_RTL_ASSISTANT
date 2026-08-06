"""
Collect procedural signal drivers.
"""

from collections import defaultdict

from app.ast import (
    ProceduralAssignment,
)


class DriverCollector:

    def collect(
        self,
        syntax_tree,
    ):

        drivers = defaultdict(list)

        self._visit(
            syntax_tree,
            drivers,
        )

        return drivers

    def _visit(
        self,
        node,
        drivers,
    ):

        if node is None:
            return

        if isinstance(
            node,
            tuple,
        ):

            for child in node:

                self._visit(
                    child,
                    drivers,
                )

            return

        if isinstance(
            node,
            ProceduralAssignment,
        ):

            drivers[
                node.target
            ].append(node)

            return

        if hasattr(
            node,
            "__dict__",
        ):

            for value in vars(
                node,
            ).values():

                self._visit(
                    value,
                    drivers,
                )

        elif hasattr(
            node,
            "__slots__",
        ):

            for slot in node.__slots__:

                self._visit(
                    getattr(
                        node,
                        slot,
                        None,
                    ),
                    drivers,
                )
