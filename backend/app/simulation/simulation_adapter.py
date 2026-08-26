"""
Simulation Adapter Interface for RIVA.
Handles simulation execution, status monitoring, and log parsing.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass(slots=True)
class SimulationResult:
    """
    Result of a simulation execution.
    """

    status: str  # PASSED, FAILED, TIMEOUT, COMPILE_ERROR
    exit_code: int
    simulator_name: str = "verilator"
    stdout: str = ""
    stderr: str = ""
    errors_count: int = 0
    warnings_count: int = 0
    vcd_path: Optional[str] = None


class SimulationAdapter:
    """
    Adapter for running external or simulated testbenches.
    """

    def analyze_simulation_logs(
        self,
        log_content: str,
        simulator_name: str = "generic",
    ) -> SimulationResult:
        """
        Parses simulation output log content to extract status, errors, and warnings.
        """
        lines = log_content.splitlines()
        errors = 0
        warnings = 0
        status = "PASSED"

        for line in lines:
            lower = line.lower()
            if "error" in lower or "fatal" in lower:
                errors += 1
            elif "warning" in lower:
                warnings += 1
            if "test failed" in lower or "assertion failed" in lower:
                status = "FAILED"

        if errors > 0 and status == "PASSED":
            status = "FAILED"

        return SimulationResult(
            status=status,
            exit_code=1 if status == "FAILED" else 0,
            simulator_name=simulator_name,
            stdout=log_content,
            errors_count=errors,
            warnings_count=warnings,
        )
