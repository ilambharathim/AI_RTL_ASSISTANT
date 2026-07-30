from app.domain.rtl_tokens import RTLToken, RTLTokenType
from app.language.systemverilog.operators import (
    OPERATORS_1,
    OPERATORS_2,
    OPERATORS_3,
    OPERATORS_4,
)
from app.parsers.rtl.character_stream import CharacterStream


class OperatorReader:

    #
    # Build one deterministic operator set used by matches()
    #
    _OPERATORS = (
        set(OPERATORS_1)
        | set(OPERATORS_2)
        | set(OPERATORS_3)
        | set(OPERATORS_4)
    )

    @staticmethod
    def matches(
        stream: CharacterStream,
    ) -> bool:

        if stream.eof():
            return False

        remaining = stream.source[stream.index:]

        #
        # Deterministically check whether ANY known operator
        # starts at the current position.
        #
        for operator in sorted(
            OperatorReader._OPERATORS,
            key=len,
            reverse=True,
        ):
            if remaining.startswith(operator):
                return True

        return False

    @staticmethod
    def read(
        stream: CharacterStream,
        diagnostics,
    ) -> RTLToken:

        location = stream.location()

        remaining = stream.source[stream.index:]

        for operator in sorted(
            OperatorReader._OPERATORS,
            key=len,
            reverse=True,
        ):

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
