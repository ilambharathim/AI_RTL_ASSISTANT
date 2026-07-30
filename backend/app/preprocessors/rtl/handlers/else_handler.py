from app.preprocessors.rtl.handlers.base_handler import BaseDirectiveHandler
from app.preprocessors.rtl.macro_table import MacroTable


class ElseHandler(BaseDirectiveHandler):

    @staticmethod
    def matches(
        line: str,
    ) -> bool:

        return line.startswith("`else")

    @staticmethod
    def handle(
        line: str,
        macro_table: MacroTable,
        enabled_stack: list[bool],
    ) -> bool:

        previous = enabled_stack.pop()

        enabled_stack.append(
            not previous
        )

        return True
