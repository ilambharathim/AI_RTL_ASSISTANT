"""
Category 12: Verification/simulation/waveform tests (T397 - T404)
"""

import pytest
from app.simulation.waveform_analyzer import WaveformAnalyzer
from app.simulation.simulation_adapter import SimulationAdapter


def test_T397_valid_simulation_log():
    log_content = "SUCCESS: Testbench completed cleanly\nCycle count: 100"
    adapter = SimulationAdapter()
    result = adapter.analyze_simulation_logs(log_content)
    assert result.status == "PASSED"


def test_T398_invalid_simulation_log():
    log_content = "ERROR: Assert failed at t=45ns in tb_top.sv\nTest failed"
    adapter = SimulationAdapter()
    result = adapter.analyze_simulation_logs(log_content)
    assert result.status == "FAILED"


def test_T399_missing_simulation_result():
    log_content = ""
    adapter = SimulationAdapter()
    result = adapter.analyze_simulation_logs(log_content)
    assert result.status == "PASSED"


def test_T400_multiple_simulation_runs():
    adapter = SimulationAdapter()
    res1 = adapter.analyze_simulation_logs("SUCCESS")
    res2 = adapter.analyze_simulation_logs("ERROR: failed")
    assert res1.status == "PASSED"
    assert res2.status == "FAILED"


def test_T401_vcd_with_one_signal():
    vcd_content = "$var wire 1 ! clk $end\n#0\n0!\n#5\n1!"
    analyzer = WaveformAnalyzer()
    events = analyzer.parse_simple_vcd(vcd_content)
    assert len(events) >= 1


def test_T402_vcd_with_multiple_signals():
    vcd_content = "$var wire 1 ! clk $end\n$var wire 1 @ rst $end\n#0\n0!\n1@\n#5\n1!\n0@"
    analyzer = WaveformAnalyzer()
    events = analyzer.parse_simple_vcd(vcd_content)
    assert len(events) >= 2


def test_T403_missing_waveform_signal():
    vcd_content = "$comment empty vcd $end"
    analyzer = WaveformAnalyzer()
    events = analyzer.parse_simple_vcd(vcd_content)
    assert len(events) == 0


def test_T404_waveform_result_consistency():
    vcd_content = "$var wire 1 ! clk $end\n#0\n0!\n#5\n1!"
    analyzer = WaveformAnalyzer()
    events1 = analyzer.parse_simple_vcd(vcd_content)
    events2 = analyzer.parse_simple_vcd(vcd_content)
    assert events1 == events2
