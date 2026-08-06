"""
Lint diagnostics.
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


RIVA6001 = DiagnosticDefinition(

    code="RIVA6001",

    category=DiagnosticCategory.LINT,

    severity=DiagnosticSeverity.WARNING,

    title="Unused Signal",

    message="Signal is never used.",

    explanation=(
        "The declared signal is never read."
    ),

    suggestion=(
        "Remove the declaration or use the signal."
    ),
)


RIVA6002 = DiagnosticDefinition(

    code="RIVA6002",

    category=DiagnosticCategory.LINT,

    severity=DiagnosticSeverity.ERROR,

    title="Multiple Drivers",

    message="Signal has multiple procedural drivers.",

    explanation=(
        "More than one procedural block assigns to the same signal."
    ),

    suggestion=(
        "Drive the signal from a single always block or redesign the logic."
    ),
)


RIVA6003 = DiagnosticDefinition(

    code="RIVA6003",

    category=DiagnosticCategory.LINT,

    severity=DiagnosticSeverity.WARNING,

    title="Constant Condition",

    message="Conditional expression is constant.",

    explanation=(
        "The condition always evaluates to the same value."
    ),

    suggestion=(
        "Remove the redundant condition or replace it with "
        "a variable expression."
    ),
)


RIVA6004 = DiagnosticDefinition(

    code="RIVA6004",

    category=DiagnosticCategory.LINT,

    severity=DiagnosticSeverity.WARNING,

    title="Dead Assignment",

    message="Assignment is overwritten before being read.",

    explanation=(
        "The assigned value is never observed because another "
        "assignment replaces it first."
    ),

    suggestion=(
        "Remove the dead assignment or verify the intended logic."
    ),
)
