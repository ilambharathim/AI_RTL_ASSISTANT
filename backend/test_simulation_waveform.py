"""
Unit tests for SimulationAdapter and WaveformAnalyzer.
"""

from app.simulation.simulation_adapter import SimulationAdapter
from app.simulation.waveform_analyzer import WaveformAnalyzer


def test_simulation_log_parsing():
    log_data = """
    [0] INFO: Starting Verilator Simulation
    [10] ERROR: Width mismatch on bus assignment
    [20] TEST FAILED: Assertion error at time 20ns
    """

    adapter = SimulationAdapter()
    result = adapter.analyze_simulation_logs(log_data, simulator_name="verilator")

    assert result.status == "FAILED"
    assert result.errors_count >= 1
    assert result.exit_code == 1


def test_vcd_waveform_analysis():
    vcd = """
    $var wire 1 ! clk $end
    $var wire 1 " rst $end
    #0
    0!
    1"
    #10
    1!
    #10
    0!
    #20
    1!
    """

    analyzer = WaveformAnalyzer()
    events = analyzer.parse_simple_vcd(vcd)

    assert len(events) >= 4
    observations = analyzer.analyze_events(events)

    glitches = [o for o in observations if o.category == "GLITCH"]
    assert len(glitches) == 1
    assert glitches[0].signal_name == "clk"
    assert glitches[0].timestamp == 10
