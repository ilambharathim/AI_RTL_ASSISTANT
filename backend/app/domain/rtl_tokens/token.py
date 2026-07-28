from dataclasses import dataclass

from app.domain.rtl_tokens.token_type import RTLTokenType
from app.shared.source_location import SourceLocation


@dataclass(slots=True, frozen=True)
class RTLToken:
    """
    Immutable token produced by the deterministic RTL lexer.
    """

    token_type: RTLTokenType
    value: str
    source_location: SourceLocation

    def __post_init__(self) -> None:
        if not isinstance(self.token_type, RTLTokenType):
            raise TypeError(
                "token_type must be an RTLTokenType."
            )

        if not isinstance(self.value, str):
            raise TypeError(
                "value must be a string."
            )

        if not isinstance(
            self.source_location,
            SourceLocation,
        ):
            raise TypeError(
                "source_location must be a SourceLocation."
            )
