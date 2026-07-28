from app.domain.rtl_tokens import RTLToken, RTLTokenType
from app.language.systemverilog.operators import (
    OPERATORS_1,
    OPERATORS_2,
    OPERATORS_3,
    OPERATORS_4,
)
from app.parsers.rtl.character_stream import CharacterStream


class OperatorReader:

    @staticmethod
    def matches(
        stream: CharacterStream,
    ) -> bool:

        if stream.eof():
            return False

        return stream.peek() in {
            "+", "-", "*", "/", "%", "=",
            "<", ">", "!", "&", "|",
            "^", "~", "?", ":", "."
        }

    @staticmethod
    def read(
        stream: CharacterStream,
        diagnostics,
    ) -> RTLToken:

        location = stream.location()

        remaining = stream.source[stream.index:]

        for table in (
            OPERATORS_4,
            OPERATORS_3,
            OPERATORS_2,
            OPERATORS_1,
        ):
            for operator in table:

                if remaining.startswith(operator):

                    for _ in operator:
                        stream.advance()

                    return RTLToken(
                        token_type=RTLTokenType.OPERATOR,
                        value=operator,
                        source_location=location,
                    )

        raise RuntimeError(
            "OperatorReader.matches() succeeded but no operator matched."
        )
