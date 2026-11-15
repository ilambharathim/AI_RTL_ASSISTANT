"""
RIVA Design Metadata Extractor.
Extracts verified design parameters, signal metadata, and operation counts from elaborated AST.
"""

from __future__ import annotations
from typing import Dict, List, Any, Optional


class DesignMetadataExtractor:
    """
    Extracts structured design metadata, signal parameters, and RTL operation counts
    from backend syntax trees.
    """

    def extract_metadata(self, syntax_tree: Any, semantic_model: Any = None) -> Dict[str, Any]:
        """
        Extracts verified design metadata dictionary.
        """
        if not syntax_tree or not hasattr(syntax_tree, "declarations") or not syntax_tree.declarations:
            return {
                "top_module": "top",
                "module_count": 0,
                "instance_count": 0,
                "port_count": 0,
                "signal_count": 0,
                "input_count": 0,
                "output_count": 0,
                "parameter_count": 0,
                "assignment_count": 0,
                "always_block_count": 0,
                "operation_counts": {
                    "AND": 0, "OR": 0, "XOR": 0, "NOT": 0,
                    "ADD": 0, "SUB": 0, "MUL": 0, "DIV": 0,
                    "COMPARE": 0, "SHIFT": 0, "MUX": 0
                },
                "signals": []
            }

        modules = syntax_tree.declarations
        top_mod = modules[0]
        top_name = getattr(top_mod, "name", "top")

        module_count = len(modules)
        instance_count = 0
        assignment_count = 0
        always_block_count = 0
        parameter_count = 0

        signals_list = []
        signal_names = set()
        input_count = 0
        output_count = 0

        op_counts = {
            "AND": 0, "OR": 0, "XOR": 0, "NOT": 0,
            "ADD": 0, "SUB": 0, "MUL": 0, "DIV": 0,
            "COMPARE": 0, "SHIFT": 0, "MUX": 0
        }

        for mod in modules:
            # Ports
            for port in getattr(mod, "ports", []):
                direction = getattr(port, "direction", "input")
                sig_name = getattr(port, "name", "")
                sig_type = getattr(port, "signal_type", "logic")
                
                width = 1
                packed = getattr(port, "packed_range", None)
                if packed:
                    try:
                        left_val = int(getattr(packed.left, "value", 0))
                        right_val = int(getattr(packed.right, "value", 0))
                        width = abs(left_val - right_val) + 1
                    except (ValueError, TypeError):
                        width = 1

                if direction == "input":
                    input_count += 1
                elif direction == "output":
                    output_count += 1

                if sig_name and sig_name not in signal_names:
                    signal_names.add(sig_name)
                    signals_list.append({
                        "name": sig_name,
                        "direction": direction,
                        "data_type": sig_type,
                        "width": width,
                        "signed": False,
                    })

            # Members
            for member in getattr(mod, "members", []):
                kind = getattr(member, "kind", "")
                if kind == "ContinuousAssign":
                    assignment_count += 1
                    self._extract_ops_from_node(getattr(member, "expression", None), op_counts)
                elif kind in ("ProceduralBlock", "AlwaysBlock"):
                    always_block_count += 1
                    self._extract_ops_from_node(getattr(member, "statement", None), op_counts)
                elif kind == "ModuleInstantiation":
                    instance_count += 1
                elif kind == "ParameterDeclaration":
                    parameter_count += 1
                elif kind in ("VariableDeclaration", "NetDeclaration"):
                    sig_name = getattr(member, "name", "")
                    if sig_name and sig_name not in signal_names:
                        signal_names.add(sig_name)
                        signals_list.append({
                            "name": sig_name,
                            "direction": "internal",
                            "data_type": getattr(member, "signal_type", "logic"),
                            "width": 1,
                            "signed": False,
                        })

        return {
            "top_module": top_name,
            "module_count": module_count,
            "instance_count": instance_count,
            "port_count": len(getattr(top_mod, "ports", [])),
            "signal_count": len(signals_list),
            "input_count": input_count,
            "output_count": output_count,
            "parameter_count": parameter_count,
            "assignment_count": assignment_count,
            "always_block_count": always_block_count,
            "operation_counts": op_counts,
            "signals": signals_list,
        }

    def _extract_ops_from_node(self, node: Any, op_counts: Dict[str, int]) -> None:
        if node is None:
            return

        op = getattr(node, "operator", None)
        if op:
            if op in ("&", "&&"):
                op_counts["AND"] += 1
            elif op in ("|", "||"):
                op_counts["OR"] += 1
            elif op == "^":
                op_counts["XOR"] += 1
            elif op in ("~", "!"):
                op_counts["NOT"] += 1
            elif op == "+":
                op_counts["ADD"] += 1
            elif op == "-":
                op_counts["SUB"] += 1
            elif op == "*":
                op_counts["MUL"] += 1
            elif op == "/":
                op_counts["DIV"] += 1
            elif op in ("==", "!=", "<", ">", "<=", ">="):
                op_counts["COMPARE"] += 1
            elif op in ("<<", ">>"):
                op_counts["SHIFT"] += 1

        kind = getattr(node, "kind", "")
        if kind == "ConditionalExpression" or hasattr(node, "condition"):
            op_counts["MUX"] += 1

        for attr in ("left", "right", "expression", "condition", "true_expr", "false_expr", "statement", "body"):
            child = getattr(node, attr, None)
            if child is not None:
                if isinstance(child, (list, tuple)):
                    for item in child:
                        self._extract_ops_from_node(item, op_counts)
                elif hasattr(child, "kind"):
                    self._extract_ops_from_node(child, op_counts)
