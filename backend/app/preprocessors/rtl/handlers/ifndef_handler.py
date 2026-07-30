from app.preprocessors.rtl.handlers.base_handler import BaseDirectiveHandler
from app.preprocessors.rtl.macro_table import MacroTable


class IfndefHandler(BaseDirectiveHandler):

    @staticmethod
    def matches(
        line: str,
    ) -> bool:

        return line.startswith("`ifndef")

    @staticmethod
    def handle(
        line: str,
        macro_table: MacroTable,
        enabled_stack: list[bool],
    ) -> bool:

        name = line.split()[1]

        enabled_stack.append(
            enabled_stack[-1]
            and not macro_table.contains(name)
        )

        return True
