from app.preprocessors.rtl.handlers.base_handler import BaseDirectiveHandler
from app.preprocessors.rtl.macro_table import MacroTable


class EndifHandler(BaseDirectiveHandler):

    @staticmethod
    def matches(
        line: str,
    ) -> bool:

        return line.startswith("`endif")

    @staticmethod
    def handle(
        line: str,
        macro_table: MacroTable,
        enabled_stack: list[bool],
    ) -> bool:

        enabled_stack.pop()

        return True
