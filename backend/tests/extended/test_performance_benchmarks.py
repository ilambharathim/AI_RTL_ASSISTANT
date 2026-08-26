"""
RIVA Performance Benchmarking Suite.
Measures parse time, semantic analysis time, elaboration time, and diagnostic reporting latency across Small, Medium, and Large RTL designs.
"""

import time
import pytest
from app.parsers.rtl.lexer import RTLLexer
from app.parsers.rtl.parser import RTLParser
from app.semantics.semantic_analyzer import SemanticAnalyzer
from app.diagnostics.diagnostic_engine import DiagnosticEngine


def generate_benchmark_rtl(module_count: int, signals_per_module: int) -> str:
    modules = []
    for m in range(module_count):
        ports = [f"input logic [15:0] in_{s}" for s in range(signals_per_module)]
        ports.extend([f"output logic [15:0] out_{s}" for s in range(signals_per_module)])
        
        assigns = [f"assign out_{s} = in_{s};" for s in range(signals_per_module)]
        
        mod_code = f"module block_{m}(\n  " + ",\n  ".join(ports) + "\n);\n  " + "\n  ".join(assigns) + "\nendmodule"
        modules.append(mod_code)
    return "\n\n".join(modules)


def test_small_design_performance_baseline():
    rtl = generate_benchmark_rtl(module_count=1, signals_per_module=5)
    
    t0 = time.perf_counter()
    tokens = RTLLexer().tokenize(rtl)
    t_lex = time.perf_counter() - t0
    
    t1 = time.perf_counter()
    parse_res = RTLParser().parse(tokens.tokens)
    t_parse = time.perf_counter() - t1
    
    t2 = time.perf_counter()
    model = SemanticAnalyzer().analyze(parse_res.syntax_tree)
    t_sem = time.perf_counter() - t2
    
    t3 = time.perf_counter()
    diags = DiagnosticEngine().analyze(model)
    t_diag = time.perf_counter() - t3
    
    total_time = t_lex + t_parse + t_sem + t_diag
    assert total_time < 0.50  # Must complete in under 500ms


def test_medium_design_performance_baseline():
    rtl = generate_benchmark_rtl(module_count=5, signals_per_module=20)
    
    t0 = time.perf_counter()
    tokens = RTLLexer().tokenize(rtl)
    parse_res = RTLParser().parse(tokens.tokens)
    model = SemanticAnalyzer().analyze(parse_res.syntax_tree)
    diags = DiagnosticEngine().analyze(model)
    total_time = time.perf_counter() - t0
    
    assert total_time < 1.50  # Must complete in under 1.5s


def test_large_design_performance_baseline():
    rtl = generate_benchmark_rtl(module_count=10, signals_per_module=40)
    
    t0 = time.perf_counter()
    tokens = RTLLexer().tokenize(rtl)
    parse_res = RTLParser().parse(tokens.tokens)
    model = SemanticAnalyzer().analyze(parse_res.syntax_tree)
    diags = DiagnosticEngine().analyze(model)
    total_time = time.perf_counter() - t0
    
    assert total_time < 3.00  # Must complete in under 3.0s
