class Parser:
    to_parse: str = ""

    def __init__(self, to_parse: str):
        self.to_parse = to_parse

    def convert_to_asm(self) -> str:
        """Convert the parsed code to assembly code"""
        return ""