"""
Typed IR Constant Propagation.
Propagates constant values into identifiers and nested expression trees.
"""

from app.ir.ir_expression import (
    IRIdentifier,
    IRLiteral,
    IRBinary,
    IRUnary,
)
from app.optimization.model.pass_result import PassResult


class TypedConstantPropagation:

    name = "typed_constant_propagation"

    def run(
        self,
        semantic_model,
        context,
    ):
        result = PassResult()
        elaboration = getattr(semantic_model, "elaboration", None)
        if not elaboration:
            return result

        constants = getattr(semantic_model, "constant_values", {})
        ir_modules = elaboration.get("ir", {}) if isinstance(elaboration, dict) else getattr(elaboration, "ir", {})

        for module in ir_modules.values():
            if hasattr(module, "statements"):
                for statement in module.statements:
                    if hasattr(statement, "expression") and statement.expression is not None:
                        new_expr, changed = self._propagate(statement.expression, constants)
                        if changed:
                            statement.expression = new_expr
                            result.changed = True

        return result

    def _propagate(self, expr, constants):
        if expr is None:
            return None, False

        if isinstance(expr, IRIdentifier):
            if expr.name in constants:
                val_str = str(constants[expr.name])
                lit = IRLiteral(val_str)
                lit.width = getattr(expr, "width", None)
                lit.location = getattr(expr, "location", None)
                return lit, True
            return expr, False

        if isinstance(expr, IRBinary):
            left, c1 = self._propagate(expr.left, constants)
            right, c2 = self._propagate(expr.right, constants)
            if c1 or c2:
                new_bin = IRBinary(expr.operator, left, right)
                new_bin.width = getattr(expr, "width", None)
                new_bin.location = getattr(expr, "location", None)
                return new_bin, True
            return expr, False

        if isinstance(expr, IRUnary):
            operand, c1 = self._propagate(expr.operand, constants)
            if c1:
                new_un = IRUnary(expr.operator, operand)
                new_un.width = getattr(expr, "width", None)
                new_un.location = getattr(expr, "location", None)
                return new_un, True
            return expr, False

        return expr, False
