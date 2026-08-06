"""
Lint Rules.
"""

from app.ast import (
    SignalDeclaration,
)

from app.diagnostics import (
    Diagnostic,
)

from app.diagnostics.catalog import (
    RIVA6001,
    RIVA6002,
    RIVA6003,
    RIVA6004,
)

from app.diagnostics.analysis.usage_collector import (
    UsageCollector,
)

from app.diagnostics.analysis.driver_collector import (
    DriverCollector,
)

from app.diagnostics.analysis.constant_condition_collector import (
    ConstantConditionCollector,
)

from app.diagnostics.analysis.dead_assignment_collector import (
    DeadAssignmentCollector,
)


class LintRules:

    name = "Lint Rules"

    def run(
        self,
        semantic_model,
    ):

        diagnostics = []

        syntax_tree = getattr(
            semantic_model,
            "syntax_tree",
            None,
        )

        if syntax_tree is None:
            return diagnostics

        #
        # Unused Signals
        #
        used = UsageCollector().collect(
            syntax_tree,
        )

        self._visit_unused(
            syntax_tree,
            used,
            diagnostics,
        )

        #
        # Multiple Drivers
        #
        drivers = DriverCollector().collect(
            syntax_tree,
        )

        for signal_name, assignments in drivers.items():

            if len(assignments) <= 1:
                continue

            diagnostics.append(

                Diagnostic(

                    code=RIVA6002.code,

                    category=RIVA6002.category,

                    severity=RIVA6002.severity,

                    message=(
                        f"Signal '{signal_name}' has multiple procedural drivers."
                    ),

                    explanation=RIVA6002.explanation,

                    suggestion=RIVA6002.suggestion,

                    location=getattr(
                        assignments[0],
                        "location",
                        None,
                    ),

                    related_locations=tuple(

                        getattr(
                            assignment,
                            "location",
                            None,
                        )

                        for assignment in assignments[1:]

                    ),

                    repairable=False,

                    confidence=100,

                )

            )

        #
        # Constant Conditions
        #
        conditions = ConstantConditionCollector().collect(
            syntax_tree,
        )

        for statement in conditions:

            diagnostics.append(

                Diagnostic(

                    code=RIVA6003.code,

                    category=RIVA6003.category,

                    severity=RIVA6003.severity,

                    message=RIVA6003.message,

                    explanation=RIVA6003.explanation,

                    suggestion=RIVA6003.suggestion,

                    location=getattr(
                        statement,
                        "location",
                        None,
                    ),

                    repairable=False,

                    confidence=100,

                )

            )

        #
        # Dead Assignments
        #
        assignments = DeadAssignmentCollector().collect(
            syntax_tree,
        )

        for assignment in assignments:

            diagnostics.append(

                Diagnostic(

                    code=RIVA6004.code,

                    category=RIVA6004.category,

                    severity=RIVA6004.severity,

                    message=(
                        f"Assignment to '{assignment.target}' is overwritten before being read."
                    ),

                    explanation=RIVA6004.explanation,

                    suggestion=RIVA6004.suggestion,

                    location=getattr(
                        assignment,
                        "location",
                        None,
                    ),

                    repairable=False,

                    confidence=100,

                )

            )

        return diagnostics

    def _visit_unused(
        self,
        node,
        used,
        diagnostics,
    ):

        if node is None:
            return

        if isinstance(
            node,
            SignalDeclaration,
        ):

            if node.name not in used:

                diagnostics.append(

                    Diagnostic(

                        code=RIVA6001.code,

                        category=RIVA6001.category,

                        severity=RIVA6001.severity,

                        message=f"Signal '{node.name}' is never used.",

                        explanation=RIVA6001.explanation,

                        suggestion=RIVA6001.suggestion,

                        location=getattr(
                            node,
                            "location",
                            None,
                        ),

                        repairable=False,

                        confidence=100,

                    )

                )

            return

        if hasattr(
            node,
            "__dict__",
        ):

            for value in vars(node).values():

                self._visit_unused(
                    value,
                    used,
                    diagnostics,
                )

        elif hasattr(
            node,
            "__slots__",
        ):

            for slot in node.__slots__:

                self._visit_unused(

                    getattr(
                        node,
                        slot,
                        None,
                    ),

                    used,

                    diagnostics,

                )
