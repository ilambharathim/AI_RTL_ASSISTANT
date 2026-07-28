"""
Central registry of deterministic RTL token readers.

The lexer iterates through this registry in order.
The order is significant because some readers recognize
lexical constructs that begin with the same character.
"""

from app.parsers.rtl.readers.comment_reader import CommentReader
from app.parsers.rtl.readers.identifier_reader import IdentifierReader
from app.parsers.rtl.readers.number_reader import NumberReader
from app.parsers.rtl.readers.string_reader import StringReader
from app.parsers.rtl.readers.operator_reader import OperatorReader
from app.parsers.rtl.readers.symbol_reader import SymbolReader


READERS = (
    CommentReader,
    IdentifierReader,
    NumberReader,
    StringReader,
    OperatorReader,
    SymbolReader,
)
