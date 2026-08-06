"""
Width diagnostics.
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


RIVA3001 = DiagnosticDefinition(

    code="RIVA3001",

    category=DiagnosticCategory.WIDTH,

    severity=DiagnosticSeverity.ERROR,

    title="Width Mismatch",

    message="Width mismatch detected.",

    explanation=(
        "The destination signal width differs from the "
        "source expression width."
    ),

    suggestion=(
        "Resize the source or destination, or explicitly "
        "slice or extend the value."
    ),
)
