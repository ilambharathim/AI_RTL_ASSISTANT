from app.parsers.specification.normalizer import DocumentNormalizer


raw_text = """



Project Title:     RIVA


Module Name:\t\tmux2to1


Inputs:



a
b
sel



Outputs:

y



"""


print("\n========== RAW ==========\n")
print(raw_text)

normalized = DocumentNormalizer.normalize(raw_text)

print("\n========== NORMALIZED ==========\n")
print(normalized)
