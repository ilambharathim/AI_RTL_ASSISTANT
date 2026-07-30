from app.preprocessors.rtl.preprocessor import RTLPreprocessor

preprocessor = RTLPreprocessor()

source = """
`define WIDTH 32

logic [`WIDTH-1:0] data;
"""

result = preprocessor.preprocess(source)

assert result.successful

assert "`WIDTH" not in result.source

assert "32-1:0" in result.source

print("RTL macro expansion test passed.")
