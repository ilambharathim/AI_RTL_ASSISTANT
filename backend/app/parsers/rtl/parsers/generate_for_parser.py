"""
SystemVerilog generate-for parser.
"""

from app.ast.generate_for import GenerateFor

from app.domain.rtl_tokens import RTLTokenType

from app.parsers.rtl.parsers.base_parser import BaseParser
from app.parsers.rtl.parsers.expression_parser import ExpressionParser
from app.parsers.rtl.parsers.generate_body_parser import GenerateBodyParser


class GenerateForParser(BaseParser):

    @staticmethod
    def matches(context):

        if context.eof():
            return False

        token = context.current()

        return (
            token.token_type == RTLTokenType.KEYWORD
            and token.value == "for"
        )

    @staticmethod
    def parse(context):

        token = context.current()

        #
        # for
        #
        context.advance()

        #
        # (
        #
        if (
            context.eof()
            or context.current().value != "("
        ):
            raise RuntimeError(
                "Expected '(' after for."
            )

        context.advance()

        #
        # Optional genvar
        #
        if (
            not context.eof()
            and context.current().token_type
            == RTLTokenType.KEYWORD
            and context.current().value == "genvar"
        ):
            context.advance()

        #
        # Loop variable
        #
        if (
            context.eof()
            or context.current().token_type
            != RTLTokenType.IDENTIFIER
        ):
            raise RuntimeError(
                "Expected loop variable."
            )

        variable = context.advance().value

        #
        # =
        #
        if (
            context.eof()
            or context.current().value != "="
        ):
            raise RuntimeError(
                "Expected '='."
            )

        context.advance()

        #
        # Initializer
        #
        initializer = ExpressionParser.parse(
            context,
        )

        #
        # ;
        #
        if (
            context.eof()
            or context.current().value != ";"
        ):
            raise RuntimeError(
                "Expected ';' after initializer."
            )

        context.advance()

        #
        # Condition
        #
        condition = ExpressionParser.parse(
            context,
        )

        #
        # ;
        #
        if (
            context.eof()
            or context.current().value != ";"
        ):
            raise RuntimeError(
                "Expected ';' after condition."
            )

        context.advance()

        #
        # Update
        #
        #
        # Generate-for update is an assignment:
        #
        #     i = i + 1
        #
        # Do not send the entire clause through
        # ExpressionParser because '=' is not a
        # binary expression operator.
        #

        if (
            context.eof()
            or context.current().token_type
            != RTLTokenType.IDENTIFIER
        ):
            raise RuntimeError(
                "Expected update variable."
            )

        update_target = context.advance().value

        if (
            context.eof()
            or context.current().value != "="
        ):
            raise RuntimeError(
                "Expected '=' in update."
            )

        context.advance()

        update_expression = ExpressionParser.parse(
            context,
        )

        #
        # Represent update as a procedural-style
        # assignment AST node.
        #
        from app.ast.procedural_assignment import (
            ProceduralAssignment,
        )

        update = ProceduralAssignment(
            target=update_target,
            operator="=",
            expression=update_expression,
        )

        #
        # )
        #
        if (
            context.eof()
            or context.current().value != ")"
        ):
            raise RuntimeError(
                "Expected ')'."
            )

        context.advance()

        #
        # Body
        #
        members = GenerateBodyParser.parse(context)

        node = GenerateFor(
            variable=variable,
            initializer=initializer,
            condition=condition,
            update=update,
            members=tuple(members),
        )

        object.__setattr__(
            node,
            "location",
            token.source_location,
        )

        return node
