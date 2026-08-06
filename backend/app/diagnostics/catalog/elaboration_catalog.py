"""
Elaboration diagnostics.
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


RIVA4001 = DiagnosticDefinition(

    code="RIVA4001",

    category=DiagnosticCategory.ELABORATION,

    severity=DiagnosticSeverity.ERROR,

    title="Module Not Found",

    message="Referenced module cannot be resolved.",

    explanation=(
        "The instantiated module does not exist in the "
        "current compilation."
    ),

    suggestion=(
        "Compile the missing module or fix the module name."
    ),
)
