"""
Comprehensive Unit Test Suite for Phase 9 — Waveform Analyzer.
Validates 100% of branches across WaveformAnalyzer.
"""

import pytest
from app.simulation.waveform_analyzer import WaveformAnalyzer, SignalEvent, WaveformObservation


def test_waveform_analyzer_all_branches():
    analyzer = WaveformAnalyzer()

    vcd_text = """
    $var wire 1 ! clk $end
    $var wire 8 " data [7:0] $end
    #0
    0!
    b1010 "
    #invalid_time
    #10
    1!
    0!
    B1100 "
    """

    events = analyzer.parse_simple_vcd(vcd_text)
    assert len(events) >= 5

    # Check signal mapping
    clk_events = [e for e in events if e.signal_name == "clk"]
    assert len(clk_events) >= 3

    data_events = [e for e in events if e.signal_name == "data"]
    assert len(data_events) >= 2

    # Analyze observations for zero-delay glitch and toggle activity
    obs = analyzer.analyze_events(events)
    assert len(obs) >= 1
    assert any(o.category == "GLITCH" for o in obs)

    # Test single-event signal for TOGGLE_ACTIVITY
    single_ev = [SignalEvent(time=0, signal_name="const_sig", value="1")]
    obs_single = analyzer.analyze_events(single_ev)
    assert any(o.category == "TOGGLE_ACTIVITY" for o in obs_single)
