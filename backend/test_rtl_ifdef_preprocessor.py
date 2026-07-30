from app.preprocessors.rtl.preprocessor import RTLPreprocessor

preprocessor = RTLPreprocessor()

source = """
`define ASIC

`ifdef ASIC
logic clk;
`else
logic test_clk;
`endif
"""

result = preprocessor.preprocess(source)

assert result.successful

assert "logic clk;" in result.source

assert "test_clk" not in result.source

print("RTL ifdef preprocessor test passed.")
