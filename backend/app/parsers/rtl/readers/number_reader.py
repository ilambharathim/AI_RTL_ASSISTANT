from app.domain.rtl_tokens import RTLToken
from app.domain.rtl_tokens import RTLTokenType
from app.engines.diagnostics.diagnostic_factory import (
    LexerDiagnosticFactory,
)
from app.parsers.rtl.character_stream import CharacterStream


class NumberReader:
    """
    Reads SystemVerilog numeric literals.

    Supports:

        - integers
        - based literals
        - signed based literals
        - real literals
        - scientific notation
        - time literals
    """

    _BASE_SPECIFIERS = {
        "b", "B",
        "o", "O",
        "d", "D",
        "h", "H",
    }

    _TIME_UNITS = {
        "s",
        "ms",
        "us",
        "ns",
        "ps",
        "fs",
    }

    @staticmethod
    def matches(
        stream: CharacterStream,
    ) -> bool:

        if stream.eof():
            return False

        return (
            stream.peek().isdigit()
            or stream.peek() == "'"
        )

    @staticmethod
    def _validate_underscore_usage(
        value: str,
    ) -> bool:
        """
        Validate underscore placement in numeric literals.
        """

        if not value:
            return False

        if value.startswith("_"):
            return False

        if value.endswith("_"):
            return False

        if "__" in value:
            return False

        return True

    @staticmethod
    def read(
        stream: CharacterStream,
        diagnostics,
    ) -> RTLToken:

        location = stream.location()

        characters: list[str] = []

        while (
            not stream.eof()
            and stream.peek().isdigit()
        ):
            characters.append(stream.advance())

        #
        # Based literal
        #
        if (
            not stream.eof()
            and stream.peek() == "'"
        ):

            characters.append(stream.advance())

            if (
                not stream.eof()
                and stream.peek() in ("s", "S")
            ):
                characters.append(stream.advance())

            if (
                stream.eof()
                or stream.peek()
                not in NumberReader._BASE_SPECIFIERS
            ):

                diagnostics.append(
                    LexerDiagnosticFactory.invalid_based_literal(
                        location
                    )
                )

                return RTLToken(
                    token_type=RTLTokenType.NUMBER,
                    value="".join(characters),
                    source_location=location,
                )

            characters.append(stream.advance())

            while (
                not stream.eof()
                and (
                    stream.peek().isalnum()
                    or stream.peek() == "_"
                )
            ):
                characters.append(stream.advance())

            return RTLToken(
                token_type=RTLTokenType.NUMBER,
                value="".join(characters),
                source_location=location,
            )

        #
        # Fraction
        #
        is_real = False

        if (
            not stream.eof()
            and stream.peek() == "."
        ):

            is_real = True

            characters.append(stream.advance())

            while (
                not stream.eof()
                and stream.peek().isdigit()
            ):
                characters.append(stream.advance())

        #
        # Exponent
        #
        if (
            not stream.eof()
            and stream.peek() in ("e", "E")
        ):

            is_real = True

            characters.append(stream.advance())

            if (
                not stream.eof()
                and stream.peek() in ("+", "-")
            ):
                characters.append(stream.advance())

            while (
                not stream.eof()
                and stream.peek().isdigit()
            ):
                characters.append(stream.advance())

        #
        # Time unit
        #
        unit = ""

        while (
            not stream.eof()
            and stream.peek().isalpha()
        ):
            unit += stream.advance()

        if unit:

            characters.append(unit)

            if unit in NumberReader._TIME_UNITS:

                return RTLToken(
                    token_type=RTLTokenType.TIME_LITERAL,
                    value="".join(characters),
                    source_location=location,
                )

        token_type = (
            RTLTokenType.REAL_NUMBER
            if is_real
            else RTLTokenType.NUMBER
        )

        return RTLToken(
            token_type=token_type,
            value="".join(characters),
            source_location=location,
        )
