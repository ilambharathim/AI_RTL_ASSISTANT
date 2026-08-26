"""
RIVA Expression Type Checker.

Infers semantic type information for expressions.

The checker supports both:
    1. canonical SemanticModel.semantic_types
    2. legacy SemanticModel.types

The legacy representation remains supported so existing
diagnostics and tests continue to work during migration.
"""

import re

from app.ast.expression import (
    IdentifierExpression,
    LiteralExpression,
    UnaryExpression,
    BinaryExpression,
    FunctionCallExpression,
)


class ExpressionTypeChecker:

    def infer(
        self,
        expression,
        model,
    ):
        #
        # Plain string — occurs in ContinuousAssign.expression when
        # the parser stored the identifier as a raw string rather
        # than wrapping it in IdentifierExpression.
        #
        if isinstance(expression, str):
            return self._lookup_type(expression, model)

        #
        # Identifier
        #
        if isinstance(
            expression,
            IdentifierExpression,
        ):
            return self._lookup_type(
                expression.name,
                model,
            )

        #
        # Integer / sized literal
        #
        if isinstance(
            expression,
            LiteralExpression,
        ):
            return self._infer_literal(
                expression.value,
            )

        #
        # Unary expression
        #
        if isinstance(
            expression,
            UnaryExpression,
        ):
            operand = self.infer(
                expression.operand,
                model,
            )

            if operand is None:
                return None

            if expression.operator not in (
                "+",
                "-",
                "~",
            ):
                return None

            return {
                "type": operand["type"],
                "width": operand["width"],
                "signed": operand["signed"],
            }

        #
        # Binary expression
        #
        if isinstance(
            expression,
            BinaryExpression,
        ):
            left = self.infer(
                expression.left,
                model,
            )

            right = self.infer(
                expression.right,
                model,
            )

            if left is None or right is None:
                return None

            return {
                "type": left["type"],
                "width": max(
                    left["width"],
                    right["width"],
                ),
                "signed": (
                    left["signed"]
                    or right["signed"]
                ),
            }

        #
        # Function calls are not yet given a concrete
        # return type by the semantic model.
        #
        # Keep this explicit rather than guessing.
        #
        if isinstance(
            expression,
            FunctionCallExpression,
        ):
            return None

        return None

    def _lookup_type(
        self,
        name,
        model,
    ):
        #
        # Canonical semantic type repository.
        #
        semantic_type = getattr(
            model,
            "semantic_types",
            {},
        ).get(name)

        if semantic_type is not None:
            return self._normalize_semantic_type(
                semantic_type,
            )

        #
        # Legacy repository.
        #
        legacy_type = getattr(
            model,
            "types",
            {},
        ).get(name)

        if legacy_type is not None:
            return self._normalize_type_info(
                legacy_type,
            )

        return None

    def _normalize_semantic_type(
        self,
        semantic_type,
    ):
        #
        # RTLType-like objects expose width/signed/packed.
        #
        width = getattr(
            semantic_type,
            "width",
            None,
        )

        signed = getattr(
            semantic_type,
            "signed",
            None,
        )

        packed = getattr(
            semantic_type,
            "packed",
            False,
        )

        name = getattr(
            semantic_type,
            "name",
            None,
        )

        if width is None:
            return None

        if signed is None:
            signed = False

        return {
            "type": name or "logic",
            "width": width,
            "signed": bool(signed),
            "packed": bool(packed),
        }

    def _normalize_type_info(
        self,
        type_info,
    ):
        #
        # Existing tests and passes use dictionaries.
        #
        if not isinstance(
            type_info,
            dict,
        ):
            width = getattr(
                type_info,
                "width",
                None,
            )

            if width is None:
                return None

            return {
                "type": getattr(
                    type_info,
                    "name",
                    "logic",
                ),
                "width": width,
                "signed": bool(
                    getattr(
                        type_info,
                        "signed",
                        False,
                    )
                ),
                "packed": bool(
                    getattr(
                        type_info,
                        "packed",
                        False,
                    )
                ),
            }

        width = type_info.get(
            "width",
        )

        if width is None:
            return None

        return {
            "type": type_info.get(
                "type",
                "logic",
            ),
            "width": width,
            "signed": bool(
                type_info.get(
                    "signed",
                    False,
                )
            ),
            "packed": bool(
                type_info.get(
                    "packed",
                    False,
                )
            ),
        }

    def _infer_literal(
        self,
        value,
    ):
        text = str(value).strip()

        #
        # Sized SystemVerilog literal:
        #
        # 8'hFF
        # 8'shFF
        # 4'b1010
        # 4'sb1010
        #
        match = re.fullmatch(
            r"(\d+)'([sS]?)([bBoOdDhH])([0-9a-fA-F_xXzZ]+)",
            text,
        )

        if match is not None:
            width = int(
                match.group(1),
            )

            signed = bool(
                match.group(2),
            )

            return {
                "type": "int",
                "width": width,
                "signed": signed,
            }

        #
        # Unsized integer literal.
        #
        if re.fullmatch(
            r"[+-]?\d+",
            text,
        ):
            return {
                "type": "int",
                "width": 32,
                "signed": True,
            }

        return None
