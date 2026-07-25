from app.parsers.specification.scanner import Scanner
from app.parsers.specification.line_reader import LineReader

text = """Project Title: RIVA
Module Name: mux2to1

Inputs:
a
b
sel

Outputs:
y
"""

scanner = Scanner(text)

reader = LineReader(scanner)

print("\n========== LINES ==========\n")

while not reader.eof():

    line = reader.next_line()

    print(repr(line))
