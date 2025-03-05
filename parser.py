class Parser:
    lines_to_parse: str = ""

    def __init__(self, to_parse: str):
        self.lines_to_parse = to_parse.split("\n")

    def convert_to_asm(self) -> str:
        """Convert the parsed code to assembly code"""
        return ""