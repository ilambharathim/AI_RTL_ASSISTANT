from app.modules.specification.reader import SpecificationReader
from app.modules.specification.parser import SpecificationParser


class SpecificationService:

    def __init__(self):

        self.reader = SpecificationReader()

        self.parser = SpecificationParser()

    def load(self, file_path: str):

        text = self.reader.read(file_path)

        return self.parser.parse(text)