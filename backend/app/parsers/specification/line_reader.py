"""
RIVA Line Reader

Reads logical lines from the generic scanner.

Future versions will support PDF, DOCX,
Markdown and OCR normalization without
changing the lexer.
"""

from app.parsers.specification.scanner import Scanner


class LineReader:

    def __init__(self, scanner: Scanner):

        self.scanner = scanner

    # -------------------------------------------------

    def eof(self):

        return self.scanner.eof()

    # -------------------------------------------------

    def next_line(self):

        if self.scanner.eof():
            return None

        chars = []

        while not self.scanner.eof():

            ch = self.scanner.current

            if ch == "\n":

                self.scanner.advance()

                break

            if ch != "\r":

                chars.append(ch)

            self.scanner.advance()

        return "".join(chars)
