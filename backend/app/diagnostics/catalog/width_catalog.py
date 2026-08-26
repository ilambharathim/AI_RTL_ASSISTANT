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

    severity=DiagnosticSeverity.WARNING,

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


RIVA3002 = DiagnosticDefinition(

    code="RIVA3002",

    category=DiagnosticCategory.WIDTH,

    severity=DiagnosticSeverity.WARNING,

    title="Signedness Mismatch",

    message="Signedness mismatch detected.",

    explanation=(
        "The signedness of the destination signal differs "
        "from the source expression."
    ),

    suggestion=(
        "Use matching signedness or explicitly cast the "
        "source expression."
    ),

)
