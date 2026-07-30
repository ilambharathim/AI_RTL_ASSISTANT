from app.preprocessors.rtl.preprocessor import RTLPreprocessor

preprocessor = RTLPreprocessor()

source = """
module adder;
assign a = b;
endmodule
"""

result = preprocessor.preprocess(source)

assert result.successful
assert "module adder;" in result.source
assert "endmodule" in result.source

print("RTL preprocessor infrastructure test passed.")
