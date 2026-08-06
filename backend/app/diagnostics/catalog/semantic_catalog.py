"""
Semantic diagnostics.
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


RIVA1001 = DiagnosticDefinition(

    code="RIVA1001",

    category=DiagnosticCategory.SEMANTIC,

    severity=DiagnosticSeverity.ERROR,

    title="Undefined Identifier",

    message="Identifier is not declared.",

    explanation=(
        "The referenced identifier does not exist in the "
        "current scope."
    ),

    suggestion=(
        "Declare the identifier or correct its spelling."
    ),
)
