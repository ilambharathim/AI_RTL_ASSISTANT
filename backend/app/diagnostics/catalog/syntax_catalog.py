"""
Syntax diagnostics.
"""

from app.diagnostics.catalog.diagnostic_catalog import (
    DiagnosticDefinition,
)

from app.diagnostics.model.categories import (
    DiagnosticCategory,
)

from app.diagnostics.model.severity import (
    DiagnosticSeverity,
)


RIVA0001 = DiagnosticDefinition(

    code="RIVA0001",

    category=DiagnosticCategory.SYNTAX,

    severity=DiagnosticSeverity.ERROR,

    title="Syntax Error",

    message="Invalid SystemVerilog syntax.",

    explanation=(
        "The parser encountered an unexpected token."
    ),

    suggestion=(
        "Correct the syntax near the reported location."
    ),
)
