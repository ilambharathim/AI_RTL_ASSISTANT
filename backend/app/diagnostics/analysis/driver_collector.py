"""
Collect procedural signal drivers.

A signal has multiple drivers only when it is assigned from more than
one distinct always block or continuous-assign statement.  Multiple
ProceduralAssignment nodes for the same target *within the same
always block* (e.g. the then- and else-branches of a single
if/else) are a single logical driver and must not be flagged.
"""

from collections import defaultdict

from app.ast import (
    AlwaysBlock,
    ProceduralAssignment,
)


class DriverCollector:

    def collect(
        self,
        syntax_tree,
    ):
        """
        Return a dict: signal_name → list[ProceduralAssignment].

        Each entry in the list is the *first* assignment from a
        distinct always block, so len > 1 means genuinely multiple
        drivers.
        """

        # signal_name -> {block_id -> first_assignment_node}
        block_map: dict[str, dict[int, ProceduralAssignment]] = defaultdict(dict)

        self._visit(
            syntax_tree,
            current_block_id=None,
            block_map=block_map,
        )

        # Convert to the shape that LintRules expects:
        # signal_name -> [first_node_per_distinct_block, ...]
        drivers: dict[str, list] = {}
        for signal, by_block in block_map.items():
            if len(by_block) > 1:
                drivers[signal] = list(by_block.values())

        return drivers

    # ------------------------------------------------------------------
    # Internal traversal
    # ------------------------------------------------------------------

    def _visit(
        self,
        node,
        current_block_id,
        block_map,
    ):
        if node is None:
            return

        if isinstance(node, tuple):
            for child in node:
                self._visit(child, current_block_id, block_map)
            return

        #
        # Entering an AlwaysBlock — give it a stable id so every
        # ProceduralAssignment inside shares the same key.
        #
        if isinstance(node, AlwaysBlock):
            block_id = id(node)
            for slot in node.__slots__:
                self._visit(
                    getattr(node, slot, None),
                    block_id,
                    block_map,
                )
            return

        #
        # ProceduralAssignment — record the first occurrence per block.
        #
        if isinstance(node, ProceduralAssignment):
            if current_block_id is None:
                # Bare procedural assignment outside an always block
                # (unusual but possible); use the node's own id.
                current_block_id = id(node)
            by_block = block_map[node.target]
            if current_block_id not in by_block:
                by_block[current_block_id] = node
            return

        #
        # Generic traversal for all other nodes.
        #
        if hasattr(node, "__dict__"):
            for value in vars(node).values():
                self._visit(value, current_block_id, block_map)

        elif hasattr(node, "__slots__"):
            for slot in node.__slots__:
                self._visit(
                    getattr(node, slot, None),
                    current_block_id,
                    block_map,
                )
