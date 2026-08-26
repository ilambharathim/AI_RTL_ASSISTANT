"""
Typed IR Constant Folding.
Folds compile-time constant binary and unary expressions into IRLiteral nodes.
"""

from app.ir.ir_expression import (
    IRLiteral,
    IRBinary,
    IRUnary,
)
from app.optimization.model.pass_result import PassResult


class TypedConstantFolding:

    name = "typed_constant_folding"

    def run(
        self,
        semantic_model,
        context,
    ):
        result = PassResult()
        elaboration = getattr(semantic_model, "elaboration", None)
        if not elaboration:
            return result

        ir_modules = elaboration.get("ir", {}) if isinstance(elaboration, dict) else getattr(elaboration, "ir", {})
        for module in ir_modules.values():
            if hasattr(module, "statements"):
                for statement in module.statements:
                    if hasattr(statement, "expression") and statement.expression is not None:
                        new_expr, local_change = self._fold(statement.expression)
                        if local_change:
                            statement.expression = new_expr
                            result.changed = True

        return result

    def _fold(self, expr):
        if expr is None:
            return None, False

        if isinstance(expr, IRBinary):
            left, c1 = self._fold(expr.left)
            right, c2 = self._fold(expr.right)
            changed = c1 or c2

            if isinstance(left, IRLiteral) and isinstance(right, IRLiteral):
                try:
                    v1 = int(str(left.value), 0)
                    v2 = int(str(right.value), 0)
                    res = None
                    op = expr.operator
                    if op == "+":
                        res = v1 + v2
                    elif op == "-":
                        res = v1 - v2
                    elif op == "*":
                        res = v1 * v2
                    elif op in ("/", "div"):
                        res = v1 // v2 if v2 != 0 else None
                    elif op == "&":
                        res = v1 & v2
                    elif op == "|":
                        res = v1 | v2
                    elif op == "^":
                        res = v1 ^ v2
                    elif op == "==":
                        res = int(v1 == v2)
                    elif op == "!=":
                        res = int(v1 != v2)
                    elif op == "<":
                        res = int(v1 < v2)
                    elif op == "<=":
                        res = int(v1 <= v2)
                    elif op == ">":
                        res = int(v1 > v2)
                    elif op == ">=":
                        res = int(v1 >= v2)

                    if res is not None:
                        lit = IRLiteral(str(res))
                        lit.width = getattr(expr, "width", None)
                        lit.location = getattr(expr, "location", None)
                        return lit, True
                except (ValueError, TypeError):
                    pass

            if changed:
                folded = IRBinary(expr.operator, left, right)
                folded.width = getattr(expr, "width", None)
                folded.location = getattr(expr, "location", None)
                return folded, True
            return expr, False

        if isinstance(expr, IRUnary):
            operand, changed = self._fold(expr.operand)
            if isinstance(operand, IRLiteral):
                try:
                    val = int(str(operand.value), 0)
                    res = None
                    op = expr.operator
                    if op == "-":
                        res = -val
                    elif op == "+":
                        res = val
                    elif op == "~":
                        res = ~val
                    elif op == "!":
                        res = int(not val)

                    if res is not None:
                        lit = IRLiteral(str(res))
                        lit.width = getattr(expr, "width", None)
                        lit.location = getattr(expr, "location", None)
                        return lit, True
                except (ValueError, TypeError):
                    pass

            if changed:
                folded = IRUnary(expr.operator, operand)
                folded.width = getattr(expr, "width", None)
                folded.location = getattr(expr, "location", None)
                return folded, True
            return expr, False

        return expr, False
