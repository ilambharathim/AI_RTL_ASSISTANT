"""
Waveform Event Analyzer.
Parses VCD value changes and evaluates temporal signal properties.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any


@dataclass(slots=True)
class SignalEvent:
    """
    Represents a value transition on a signal at a given simulation timestamp.
    """

    time: int
    signal_name: str
    value: str


@dataclass(slots=True)
class WaveformObservation:
    """
    Observation derived from waveform analysis.
    """

    category: str  # TOGGLE_ACTIVITY, GLITCH, TIMING, ASSERTION
    signal_name: str
    message: str
    timestamp: int = 0


class WaveformAnalyzer:
    """
    Analyzes signal value transitions and temporal properties from event traces.
    """

    def analyze_vcd_text(self, vcd_text: str) -> Dict[str, Any]:
        """
        Parses and analyzes VCD text, returning a structured summary dict
        suitable for API payload and evidence store.
        """
        if not vcd_text or not vcd_text.strip():
            return {
                "status": "empty",
                "events_count": 0,
                "observations": [],
                "observations_raw": [],
                "signals_analyzed": [],
            }

        try:
            events = self.parse_simple_vcd(vcd_text)
            observations = self.analyze_events(events)

            obs_list = [
                {
                    "category": obs.category,
                    "signal_name": obs.signal_name,
                    "message": obs.message,
                    "timestamp": obs.timestamp,
                }
                for obs in observations
            ]

            signals = sorted(list({e.signal_name for e in events}))

            return {
                "status": "success",
                "events_count": len(events),
                "observations": obs_list,
                "observations_raw": observations,
                "signals_analyzed": signals,
            }
        except Exception as exc:
            err_obs = WaveformObservation(
                category="PARSING_ERROR",
                signal_name="<unknown>",
                message=f"Malformed VCD input: {str(exc)}",
                timestamp=0,
            )
            return {
                "status": "error",
                "events_count": 0,
                "observations": [
                    {
                        "category": err_obs.category,
                        "signal_name": err_obs.signal_name,
                        "message": err_obs.message,
                        "timestamp": 0,
                    }
                ],
                "observations_raw": [err_obs],
                "signals_analyzed": [],
            }

    def parse_simple_vcd(self, vcd_text: str) -> List[SignalEvent]:
        """
        Extracts value change events from a basic VCD trace.
        """
        events: List[SignalEvent] = []
        current_time = 0
        signal_map: Dict[str, str] = {}

        tokens = vcd_text.split()
        idx = 0
        n = len(tokens)
        in_header = True

        while idx < n:
            tok = tokens[idx]

            if in_header:
                if tok == "$enddefinitions" or (tok.startswith("#") and len(tok) > 1 and tok[1:].isdigit()):
                    in_header = False
                elif tok == "$var":
                    if idx + 4 < n:
                        symbol = tokens[idx + 3]
                        name = tokens[idx + 4]
                        signal_map[symbol] = name
                    idx += 1
                    continue
                else:
                    idx += 1
                    continue

            # Body value changes (timestamp: #0, #10 ...)
            if tok.startswith("#") and len(tok) > 1 and tok[1:].isdigit():
                try:
                    current_time = int(tok[1:])
                except ValueError:
                    pass
                idx += 1
                continue

            elif tok.startswith("b") or tok.startswith("B"):
                val = tok[1:]
                if (
                    idx + 1 < n
                    and not (tokens[idx + 1].startswith("#") and len(tokens[idx + 1]) > 1 and tokens[idx + 1][1:].isdigit())
                    and not tokens[idx + 1].startswith("$")
                ):
                    symbol = tokens[idx + 1]
                    name = signal_map.get(symbol, symbol)
                    events.append(SignalEvent(time=current_time, signal_name=name, value=val))
                    idx += 2
                    continue
                idx += 1
                continue

            elif len(tok) >= 2 and tok[0] in "01xXzZ":
                val = tok[0]
                symbol = tok[1:]
                name = signal_map.get(symbol, symbol)
                events.append(SignalEvent(time=current_time, signal_name=name, value=val))
                idx += 1
                continue
            idx += 1

        return events

    def analyze_events(self, events: List[SignalEvent]) -> List[WaveformObservation]:
        """
        Analyzes event history for inactive signals, glitches, or unexpected toggles.
        """
        observations: List[WaveformObservation] = []
        signal_counts: Dict[str, int] = {}
        last_event: Dict[str, SignalEvent] = {}

        for ev in events:
            signal_counts[ev.signal_name] = signal_counts.get(ev.signal_name, 0) + 1
            if ev.signal_name in last_event:
                prev = last_event[ev.signal_name]
                # Check for zero-delay glitch (multiple transitions at exact same timestamp)
                if prev.time == ev.time and prev.value != ev.value:
                    observations.append(
                        WaveformObservation(
                            category="GLITCH",
                            signal_name=ev.signal_name,
                            message=f"Zero-delay glitch detected on signal '{ev.signal_name}' at time {ev.time}.",
                            timestamp=ev.time,
                        )
                    )
            last_event[ev.signal_name] = ev

        for sig, count in signal_counts.items():
            if count == 1:
                observations.append(
                    WaveformObservation(
                        category="TOGGLE_ACTIVITY",
                        signal_name=sig,
                        message=f"Signal '{sig}' had no dynamic toggle activity during simulation trace.",
                        timestamp=0,
                    )
                )

        return observations
