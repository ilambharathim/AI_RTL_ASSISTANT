"""
Waveform Event Analyzer.
Parses VCD value changes and evaluates temporal signal properties.
"""

from __future__ import annotations
import re
from dataclasses import dataclass
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

    def analyze_vcd_text(self, vcd_text: str, source: str = "uploaded") -> Dict[str, Any]:
        """
        Parses and analyzes VCD text, returning a structured summary dict
        suitable for API payload and evidence store.
        """
        if not vcd_text or not vcd_text.strip():
            return {
                "status": "empty",
                "source": "none",
                "events_count": 0,
                "events": [],
                "observations": [],
                "observations_raw": [],
                "signals_analyzed": [],
                "simulation": {
                    "timescale": "1ns",
                    "start_time": 0,
                    "end_time": 0,
                    "duration": 0,
                    "clock_signals": [],
                    "clock_periods": {},
                    "clock_frequencies": {},
                },
                "signal_activity": {},
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
            events_dict = [
                {
                    "signal": e.signal_name,
                    "timestamp": e.time,
                    "value": e.value,
                }
                for e in events
            ]

            sim_meta, signal_activity = self.compute_simulation_metadata(events, vcd_text)

            return {
                "status": "success",
                "source": source,
                "events_count": len(events),
                "events": events_dict,
                "observations": obs_list,
                "observations_raw": observations,
                "signals_analyzed": signals,
                "simulation": sim_meta,
                "signal_activity": signal_activity,
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
                "source": source,
                "events_count": 0,
                "events": [],
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
                "simulation": {
                    "timescale": "1ns",
                    "start_time": 0,
                    "end_time": 0,
                    "duration": 0,
                    "clock_signals": [],
                    "clock_periods": {},
                    "clock_frequencies": {},
                },
                "signal_activity": {},
            }

    def compute_simulation_metadata(self, events: List[SignalEvent], vcd_text: str) -> tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Calculates simulation time bounds, clock periods, frequencies, and transition activity.
        """
        if not events:
            return {
                "timescale": "1ns",
                "start_time": 0,
                "end_time": 0,
                "duration": 0,
                "clock_signals": [],
                "clock_periods": {},
                "clock_frequencies": {},
            }, {}

        timescale_match = re.search(r'\$timescale\s+([^\$]+)\$end', vcd_text)
        timescale = timescale_match.group(1).strip() if timescale_match else "1ns"

        start_time = min(e.time for e in events)
        end_time = max(e.time for e in events)
        duration = end_time - start_time

        signal_activity: Dict[str, Dict[str, int]] = {}
        signal_events: Dict[str, List[SignalEvent]] = {}

        for e in events:
            sig = e.signal_name
            if sig not in signal_activity:
                signal_activity[sig] = {"transitions": 0}
                signal_events[sig] = []
            signal_activity[sig]["transitions"] += 1
            signal_events[sig].append(e)

        clock_signals = []
        clock_periods: Dict[str, int] = {}
        clock_frequencies: Dict[str, str] = {}

        for sig, evs in signal_events.items():
            if sig.lower() in ("clk", "clock", "sys_clk", "clk_i") or "clk" in sig.lower():
                rising_edges = [ev.time for ev in evs if ev.value in ('1', 'b1')]
                if len(rising_edges) >= 2:
                    periods = [rising_edges[i] - rising_edges[i-1] for i in range(1, len(rising_edges))]
                    if len(periods) > 0:
                        period = periods[0]
                        if period > 0:
                            clock_signals.append(sig)
                            clock_periods[sig] = period
                            freq_mhz = 1000.0 / period
                            clock_frequencies[sig] = f"{freq_mhz:.1f} MHz"

        simulation = {
            "timescale": timescale,
            "start_time": start_time,
            "end_time": end_time,
            "duration": duration,
            "clock_signals": clock_signals,
            "clock_periods": clock_periods,
            "clock_frequencies": clock_frequencies,
        }

        return simulation, signal_activity

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
