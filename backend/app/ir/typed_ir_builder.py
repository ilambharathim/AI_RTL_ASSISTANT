"""
Typed IR Builder.

Builds the Typed Intermediate Representation (IR)
from the semantic AST.
"""

from app.ast import (
    CompilationUnit,
    ModuleDeclaration,
    ProceduralAssignment,
    IfStatement,
    StatementBlock,
    AlwaysBlock,
)

from app.ast.expression import (
    IdentifierExpression,
    LiteralExpression,
    UnaryExpression,
    BinaryExpression,
    FunctionCallExpression,
)

from app.ir.ir_module import IRModule

from app.ir.ir_statement import (
    IRAssignment,
    IRIf,
    IRAlways,
    IRBlock,
)

from app.ir.ir_expression import (
    IRIdentifier,
    IRLiteral,
    IRUnary,
    IRBinary,
    IRFunctionCall,
)


class TypedIRBuilder:

    def build(
        self,
        syntax_tree,
        semantic_model,
    ):

        modules = {}

        if not isinstance(
            syntax_tree,
            CompilationUnit,
        ):
            return modules

        for declaration in syntax_tree.declarations:

            if isinstance(
                declaration,
                ModuleDeclaration,
            ):

                module = self._module(
                    declaration,
                )

                modules[
                    module.name
                ] = module

        if isinstance(semantic_model.elaboration, dict):
            semantic_model.elaboration["ir"] = modules
        elif semantic_model.elaboration is not None:
            semantic_model.elaboration.ir = modules

        return modules

    def _module(
        self,
        module,
    ):

        ir_module = IRModule(
            module.name,
        )

        for member in module.members:

            statement = self._statement(
                member,
            )

            if statement is not None:

                ir_module.statements.append(
                    statement,
                )

        return ir_module

    def _statement(
        self,
        node,
    ):

        if isinstance(
            node,
            ProceduralAssignment,
        ):

            return IRAssignment(

                target=node.target,

                expression=self._expression(
                    node.expression,
                ),

                blocking=getattr(node, "blocking", True),

            )

        if isinstance(
            node,
            IfStatement,
        ):

            return IRIf(

                condition=self._expression(
                    node.condition,
                ),

                then_branch=self._statement(
                    node.then_branch,
                ),

                else_branch=(
                    self._statement(
                        node.else_branch,
                    )
                    if node.else_branch
                    else None
                ),

            )

        if isinstance(
            node,
            StatementBlock,
        ):

            statements = []

            for statement in node.statements:

                ir = self._statement(
                    statement,
                )

                if ir is not None:

                    statements.append(
                        ir,
                    )

            return IRBlock(
                statements,
            )

        if isinstance(
            node,
            AlwaysBlock,
        ):

            return IRAlways(

                block_type=node.block_type,

                sensitivity=node.sensitivity,

                body=IRBlock(

                    [

                        self._statement(s)

                        for s in node.statements

                        if self._statement(s) is not None

                    ]

                ),

            )

        return None

    def _expression(
        self,
        node,
    ):

        if isinstance(
            node,
            IdentifierExpression,
        ):

            return IRIdentifier(
                node.name,
            )

        if isinstance(
            node,
            LiteralExpression,
        ):

            return IRLiteral(
                node.value,
            )

        if isinstance(
            node,
            UnaryExpression,
        ):

            return IRUnary(

                node.operator,

                self._expression(
                    node.operand,
                ),

            )

        if isinstance(
            node,
            BinaryExpression,
        ):

            return IRBinary(

                node.operator,

                self._expression(
                    node.left,
                ),

                self._expression(
                    node.right,
                ),

            )

        if isinstance(
            node,
            FunctionCallExpression,
        ):

            return IRFunctionCall(

                node.function_name,

                tuple(

                    self._expression(
                        argument,
                    )

                    for argument in node.arguments

                ),

            )

        return None
