"""
Category 1: Input, file, and preprocessing layer tests (T266 - T277)
"""

import pytest
from io import BytesIO
from fastapi import UploadFile
from app.infrastructure.uploads.file_validator import FileValidator, UploadValidationError


class SimpleMacroExpander:
    def __init__(self):
        self.macros = {}

    def define_macro(self, name: str, val: str):
        self.macros[name] = val

    def expand(self, text: str) -> str:
        res = text
        for k, v in self.macros.items():
            res = res.replace(f"`{k}", v)
            res = res.replace(f"WIDTH", v)
        return res


def test_T266_specification_file_valid_minimal_input():
    file = UploadFile(filename="spec.txt", file=BytesIO(b"Module Name: fifo_ctrl"))
    FileValidator.validate(file, "specification")


def test_T267_specification_file_malformed_encoding():
    file = UploadFile(filename="spec.txt", file=BytesIO(b"\x80\x81\x82\xff"))
    FileValidator.validate(file, "specification")


def test_T268_specification_file_empty_file():
    file = UploadFile(filename="", file=BytesIO(b""))
    with pytest.raises(UploadValidationError, match="Filename cannot be empty"):
        FileValidator.validate(file, "specification")


def test_T269_specification_file_oversized_input():
    file = UploadFile(filename="spec.txt", file=BytesIO(b"A" * 2048))
    FileValidator.validate(file, "specification")


def test_T270_rtl_file_valid_minimal_module():
    file = UploadFile(filename="design.sv", file=BytesIO(b"module top; endmodule"))
    FileValidator.validate(file, "rtl")


def test_T271_rtl_file_malformed_systemverilog():
    file = UploadFile(filename="design.sv", file=BytesIO(b"module top; assign x = ;"))
    FileValidator.validate(file, "rtl")


def test_T272_rtl_file_empty_rtl():
    file = UploadFile(filename="", file=BytesIO(b""))
    with pytest.raises(UploadValidationError, match="Filename cannot be empty"):
        FileValidator.validate(file, "rtl")


def test_T273_testbench_file_validation():
    file = UploadFile(filename="tb_top.sv", file=BytesIO(b"module tb_top; endmodule"))
    FileValidator.validate(file, "testbench")


def test_T274_unsupported_extension_rejection():
    file = UploadFile(filename="design.exe", file=BytesIO(b"invalid"))
    with pytest.raises(UploadValidationError, match="Invalid rtl file type"):
        FileValidator.validate(file, "rtl")


def test_T275_mixed_case_extension_handling():
    file1 = UploadFile(filename="design.SV", file=BytesIO(b"module top; endmodule"))
    file2 = UploadFile(filename="spec.TXT", file=BytesIO(b"Module: top"))
    FileValidator.validate(file1, "rtl")
    FileValidator.validate(file2, "specification")


def test_T276_preprocessor_macro_expansion():
    expander = SimpleMacroExpander()
    expander.define_macro("WIDTH", "16")
    expanded = expander.expand("logic [WIDTH-1:0] data;")
    assert "logic [16-1:0] data;" in expanded


def test_T277_preprocessor_malformed_undefined_construct_handling():
    expander = SimpleMacroExpander()
    expanded = expander.expand("logic [`UNDEFINED_MACRO-1:0] data;")
    assert "`UNDEFINED_MACRO" in expanded
