"""
Specification-to-RTL Requirement Tracer.
Links SpecificationIR requirements directly to elaborated RTL hierarchy and semantic symbols.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from app.domain.requirement import Requirement
from app.diagnostics.diagnostic import Diagnostic
from app.shared.source_location import SourceLocation


@dataclass(slots=True)
class TraceabilityLink:
    """
    Links a specification requirement to an RTL construct.
    """

    requirement_id: str
    target_signal: str
    target_module: str
    status: str  # PASSED, FAILED, UNVERIFIED
    details: str = ""
    location: SourceLocation = field(default_factory=SourceLocation)


class RequirementTracer:
    """
    Traces specification requirements against RTL symbols and semantic models.
    """

    def _collect_all_signals(self, semantic_model) -> Dict[str, int]:
        signals: Dict[str, int] = {}
        syntax_tree = getattr(semantic_model, "syntax_tree", None)
        if syntax_tree and hasattr(syntax_tree, "declarations"):
            for decl in syntax_tree.declarations:
                if hasattr(decl, "ports") and decl.ports:
                    for port in decl.ports:
                        w = 1
                        if hasattr(port, "packed_range") and port.packed_range:
                            try:
                                l = int(port.packed_range.left.value)
                                r = int(port.packed_range.right.value)
                                w = abs(l - r) + 1
                            except (AttributeError, ValueError, TypeError):
                                w = 1
                        signals[port.name] = w
                if hasattr(decl, "members") and decl.members:
                    for member in decl.members:
                        if hasattr(member, "name") and hasattr(member, "signal_type"):
                            w = 1
                            if hasattr(member, "packed_range") and member.packed_range:
                                try:
                                    l = int(member.packed_range.left.value)
                                    r = int(member.packed_range.right.value)
                                    w = abs(l - r) + 1
                                except (AttributeError, ValueError, TypeError):
                                    w = 1
                            signals[member.name] = w
        symbols = getattr(semantic_model, "symbols", {})
        for name in symbols:
            if name not in signals:
                signals[name] = 1
        return signals

    def trace(
        self,
        requirements: List[Requirement],
        semantic_model: object,
    ) -> Dict[str, object]:
        links: List[TraceabilityLink] = []
        diagnostics: List[Diagnostic] = []

        all_signals = self._collect_all_signals(semantic_model)

        for req in requirements:
            # Extract target signal candidates from requirement condition or description
            target_signal = self._extract_target_signal(req)
            if not target_signal:
                links.append(
                    TraceabilityLink(
                        requirement_id=req.requirement_id,
                        target_signal="<unknown>",
                        target_module="<top>",
                        status="UNVERIFIED",
                        details="No target signal identified in requirement.",
                        location=req.source_location,
                    )
                )
                continue

            if target_signal in all_signals:
                actual_width = all_signals[target_signal]
                expected_width = self._extract_expected_width(req)

                if expected_width is not None and actual_width != expected_width:
                    status = "FAILED"
                    details = f"Width mismatch: requirement expected {expected_width} bits, RTL has {actual_width} bits."
                    diagnostics.append(
                        Diagnostic(
                            code="RIVA6001",
                            category="specification",
                            severity="error",
                            message=f"Specification mismatch for {req.requirement_id}: {details}",
                            suggestion="Update RTL signal width to match specification requirement.",
                            location=req.source_location,
                        )
                    )
                else:
                    status = "PASSED"
                    details = f"Bound to signal '{target_signal}' ({actual_width} bits)."

                links.append(
                    TraceabilityLink(
                        requirement_id=req.requirement_id,
                        target_signal=target_signal,
                        target_module="<top>",
                        status=status,
                        details=details,
                        location=req.source_location,
                    )
                )
            else:
                status = "FAILED"
                details = f"Target signal '{target_signal}' specified in {req.requirement_id} was not found in RTL."
                diagnostics.append(
                    Diagnostic(
                        code="RIVA6002",
                        category="specification",
                        severity="error",
                        message=f"Missing signal for requirement {req.requirement_id}: signal '{target_signal}' not found in RTL.",
                        suggestion=f"Declare signal '{target_signal}' in RTL.",
                        location=req.source_location,
                    )
                )
                links.append(
                    TraceabilityLink(
                        requirement_id=req.requirement_id,
                        target_signal=target_signal,
                        target_module="<top>",
                        status=status,
                        details=details,
                        location=req.source_location,
                    )
                )

        return {
            "links": links,
            "diagnostics": diagnostics,
        }

    def _extract_target_signal(self, req: Requirement) -> Optional[str]:
        if req.condition:
            if ":" in req.condition:
                return req.condition.split(":")[0].strip()
            return req.condition.strip()
        return None


    def _extract_expected_width(self, req: Requirement) -> Optional[int]:
        text = f"{req.description or ''} {req.expected_result or ''}"
        if "bit" in text.lower():
            import re
            match = re.search(r'(\d+)\s*-\s*bit|(\d+)\s*bit', text, re.IGNORECASE)
            if match:
                val = match.group(1) or match.group(2)
                return int(val)
        return None
