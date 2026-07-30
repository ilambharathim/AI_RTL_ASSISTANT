from app.preprocessors.rtl.preprocessor import RTLPreprocessor

preprocessor = RTLPreprocessor()

source = """
`define WIDTH 32

module adder;

endmodule
"""

result = preprocessor.preprocess(source)

assert result.successful

assert "`define" not in result.source

assert "module adder;" in result.source

assert preprocessor._macros.contains("WIDTH")

assert preprocessor._macros.lookup("WIDTH") == "32"

print("RTL define preprocessor test passed.")
