"""
Generate block elaborator.

Expands generate constructs without modifying the AST.
"""

from app.ast import (
    GenerateBlock,
    GenerateIf,
    GenerateFor,
)

from app.ast.expression import (
    LiteralExpression,
    IdentifierExpression,
)

from app.elaboration.utils.ast_cloner import ASTCloner
from app.elaboration.utils.generate_substituter import (
    GenerateSubstituter,
)


class GenerateElaborator:

    def elaborate(
        self,
        syntax_tree,
        semantic_model,
    ):

        semantic_model.elaboration.elaborated_modules = {}

        for declaration in syntax_tree.declarations:

            if not hasattr(
                declaration,
                "members",
            ):
                continue

            semantic_model.elaboration.elaborated_modules[
                declaration.name
            ] = self._expand_members(
                declaration.members,
                semantic_model,
            )

    def _expand_members(
        self,
        members,
        semantic_model,
    ):

        expanded = []

        for member in members:

            if isinstance(
                member,
                GenerateBlock,
            ):

                expanded.extend(
                    self._generate_block(
                        member,
                        semantic_model,
                    )
                )

            else:

                expanded.append(
                    member,
                )

        return expanded

    def _generate_block(
        self,
        block,
        semantic_model,
    ):

        expanded = []

        for member in block.members:

            if isinstance(
                member,
                GenerateIf,
            ):

                expanded.extend(
                    self._generate_if(
                        member,
                        semantic_model,
                    )
                )

            elif isinstance(
                member,
                GenerateFor,
            ):

                expanded.extend(
                    self._generate_for(
                        member,
                        semantic_model,
                    )
                )

            else:

                expanded.append(
                    member,
                )

        return expanded

    def _generate_if(
        self,
        node,
        semantic_model,
    ):

        value = self._evaluate(
            node.condition,
            semantic_model,
        )

        if value:
            return list(
                node.true_members,
            )

        return list(
            node.false_members,
        )

    def _generate_for(
        self,
        node,
        semantic_model,
    ):

        start = self._evaluate(
            node.initializer,
            semantic_model,
        )

        limit = self._evaluate(
            node.condition,
            semantic_model,
        )

        if (
            not isinstance(start, int)
            or not isinstance(limit, int)
        ):
            return list(
                node.members,
            )

        expanded = []

        for i in range(
            start,
            limit,
        ):

            for member in node.members:

                clone = ASTCloner.clone(
                    member,
                )

                GenerateSubstituter.substitute(
                    clone,
                    node.variable,
                    i,
                )

                if hasattr(
                    clone,
                    "instance_name",
                ):

                    object.__setattr__(
                        clone,
                        "instance_name",
                        f"{clone.instance_name}_{i}",
                    )

                expanded.append(
                    clone,
                )

        return expanded

    def _evaluate(
        self,
        expression,
        semantic_model,
    ):

        if isinstance(
            expression,
            LiteralExpression,
        ):

            try:
                return int(
                    expression.value,
                )
            except ValueError:
                return 0

        if isinstance(
            expression,
            IdentifierExpression,
        ):

            return semantic_model.constant_values.get(
                expression.name,
                0,
            )

        return 0

