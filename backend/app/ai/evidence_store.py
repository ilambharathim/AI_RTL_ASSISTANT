"""
RIVA Evidence Store.
Consolidates all deterministic analysis findings into a structured evidence payload.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Any

from app.diagnostics.diagnostic import Diagnostic
from app.analysis.traceability.requirement_tracer import TraceabilityLink
from app.simulation.simulation_adapter import SimulationResult
from app.simulation.waveform_analyzer import WaveformObservation


@dataclass(slots=True)
class EvidencePayload:
    """
    Structured evidence container that feeds into AI interpretation and report generation.
    """

    project_name: str
    diagnostics: List[Diagnostic] = field(default_factory=list)
    traceability_links: List[TraceabilityLink] = field(default_factory=list)
    simulation_results: List[SimulationResult] = field(default_factory=list)
    waveform_observations: List[WaveformObservation] = field(default_factory=list)
    hierarchy_summary: Dict[str, Any] = field(default_factory=dict)
    knowledge_context: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "project_name": self.project_name,
            "total_diagnostics": len(self.diagnostics),
            "errors_count": len([d for d in self.diagnostics if d.severity == "error"]),
            "warnings_count": len([d for d in self.diagnostics if d.severity == "warning"]),
            "diagnostics": [
                {
                    "code": d.code,
                    "category": d.category,
                    "severity": d.severity,
                    "message": d.message,
                    "suggestion": d.suggestion,
                    "location": str(d.location) if d.location else "<unknown>",
                }
                for d in self.diagnostics
            ],
            "traceability": [
                {
                    "req_id": t.requirement_id,
                    "signal": t.target_signal,
                    "status": t.status,
                    "details": t.details,
                }
                for t in self.traceability_links
            ],
            "simulation": [
                {
                    "status": s.status,
                    "simulator": s.simulator_name,
                    "errors": s.errors_count,
                    "warnings": s.warnings_count,
                }
                for s in self.simulation_results
            ],
            "waveform": [
                {
                    "category": w.category,
                    "signal": w.signal_name,
                    "message": w.message,
                    "timestamp": w.timestamp,
                }
                for w in self.waveform_observations
            ],
            "hierarchy": self.hierarchy_summary,
            "knowledge": self.knowledge_context,
        }


class EvidenceStore:
    """
    Collects and manages deterministic evidence payload objects.
    """

    def __init__(self, project_name: str = "RIVA_Design"):
        self.project_name = project_name
        self.payload = EvidencePayload(project_name=project_name)

    def add_diagnostics(self, diagnostics: List[Diagnostic]) -> None:
        self.payload.diagnostics.extend(diagnostics)

    def add_traceability_links(self, links: List[TraceabilityLink]) -> None:
        self.payload.traceability_links.extend(links)

    def add_simulation_result(self, result: SimulationResult) -> None:
        self.payload.simulation_results.append(result)

    def add_waveform_observations(self, observations: List[WaveformObservation]) -> None:
        self.payload.waveform_observations.extend(observations)

    def set_hierarchy_summary(self, summary: Dict[str, Any]) -> None:
        self.payload.hierarchy_summary = summary

    def add_knowledge_context(self, text: str) -> None:
        self.payload.knowledge_context.append(text)

    def get_payload(self) -> EvidencePayload:
        return self.payload
