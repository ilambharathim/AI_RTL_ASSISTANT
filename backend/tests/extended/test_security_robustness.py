"""
RIVA Security & Input Robustness Verification Suite.
Validates protection against path traversal, null bytes, oversized payloads, and deeply nested AST expressions.
"""

import pytest
from io import BytesIO
from fastapi import UploadFile
from app.infrastructure.uploads.file_validator import FileValidator, UploadValidationError
from app.parsers.rtl.lexer import RTLLexer
from app.parsers.rtl.parser import RTLParser
from app.semantics.semantic_analyzer import SemanticAnalyzer
from app.diagnostics.diagnostic_engine import DiagnosticEngine


def test_path_traversal_filename_rejection():
    file1 = UploadFile(filename="../../evil.sv", file=BytesIO(b"module top; endmodule"))
    with pytest.raises(UploadValidationError, match="directory paths"):
        FileValidator.validate(file1, "rtl")
        
    file2 = UploadFile(filename="../../../etc/passwd", file=BytesIO(b"root:x:0:0"))
    with pytest.raises(UploadValidationError, match="directory paths"):
        FileValidator.validate(file2, "rtl")


def test_null_byte_filename_rejection():
    file_null = UploadFile(filename="design\x00evil.sv", file=BytesIO(b"module top; endmodule"))
    with pytest.raises(UploadValidationError, match="null character"):
        FileValidator.validate(file_null, "rtl")


def test_oversized_rtl_input_processing():
    lines = ["module big_design("]
    for i in range(100):
        lines.append(f"  input logic [15:0] in_{i},")
        lines.append(f"  output logic [15:0] out_{i},")
    lines.append("  input logic clk\n);")
    for i in range(100):
        lines.append(f"  assign out_{i} = in_{i};")
    lines.append("endmodule")
    
    big_rtl = "\n".join(lines)
    
    tokens = RTLLexer().tokenize(big_rtl)
    assert len(tokens.tokens) > 500
    
    parse_res = RTLParser().parse(tokens.tokens)
    assert parse_res.syntax_tree is not None
    
    model = SemanticAnalyzer().analyze(parse_res.syntax_tree)
    diags = DiagnosticEngine().analyze(model)
    assert len(diags) == 0


def test_deeply_nested_expressions_resilience():
    expr = "a"
    for i in range(50):
        expr = f"({expr} + in_{i})"
    code = f"module top(input logic [15:0] in_0, a, output logic [15:0] out); assign out = {expr}; endmodule"
    
    tokens = RTLLexer().tokenize(code)
    parse_res = RTLParser().parse(tokens.tokens)
    assert parse_res.syntax_tree is not None
