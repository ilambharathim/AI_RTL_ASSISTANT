"""
Deterministic RTL preprocessor.

Version 5

Directive-dispatch architecture.
"""

from app.engines.diagnostics.diagnostic import Diagnostic
from app.preprocessors.rtl.handler_registry import DIRECTIVE_HANDLERS
from app.preprocessors.rtl.macro_table import MacroTable
from app.preprocessors.rtl.preprocessor_result import RTLPreprocessorResult


class RTLPreprocessor:

    def __init__(self):

        self._macros = MacroTable()

    def preprocess(
        self,
        source: str,
    ) -> RTLPreprocessorResult:

        diagnostics: list[Diagnostic] = []

        output: list[str] = []

        enabled_stack = [True]

        #
        # Pass 1
        # Execute directives.
        #
        for raw_line in source.splitlines():

            line = raw_line.strip()

            handled = False

            for handler in DIRECTIVE_HANDLERS:

                if handler.matches(line):

                    handler.handle(
                        line,
                        self._macros,
                        enabled_stack,
                    )

                    handled = True

                    break

            if handled:
                continue

            if enabled_stack[-1]:
                output.append(raw_line)

        #
        # Pass 2
        # Expand object-like macros.
        #
        expanded: list[str] = []

        for line in output:

            for name, value in self._macros._table.items():

                line = line.replace(
                    f"`{name}",
                    value,
                )

            expanded.append(line)

        return RTLPreprocessorResult(
            source="\n".join(expanded),
            diagnostics=tuple(diagnostics),
        )
