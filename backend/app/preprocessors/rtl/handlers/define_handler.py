from app.preprocessors.rtl.handlers.base_handler import BaseDirectiveHandler
from app.preprocessors.rtl.macro_table import MacroTable


class DefineHandler(BaseDirectiveHandler):

    @staticmethod
    def matches(
        line: str,
    ) -> bool:

        return line.startswith("`define")

    @staticmethod
    def handle(
        line: str,
        macro_table: MacroTable,
        enabled_stack: list[bool],
    ) -> bool:

        if not enabled_stack[-1]:
            return True

        parts = line.split(maxsplit=2)

        if len(parts) >= 2:

            value = ""

            if len(parts) == 3:
                value = parts[2]

            macro_table.define(
                parts[1],
                value,
            )

        return True
