"""
Registry of deterministic preprocessor directive handlers.
"""

from app.preprocessors.rtl.handlers.define_handler import DefineHandler
from app.preprocessors.rtl.handlers.ifdef_handler import IfdefHandler
from app.preprocessors.rtl.handlers.ifndef_handler import IfndefHandler
from app.preprocessors.rtl.handlers.else_handler import ElseHandler
from app.preprocessors.rtl.handlers.endif_handler import EndifHandler

DIRECTIVE_HANDLERS = (
    DefineHandler,
    IfdefHandler,
    IfndefHandler,
    ElseHandler,
    EndifHandler,
)
