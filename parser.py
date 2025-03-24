from basetoken import BaseToken
from utils import *

class Parser:
    to_parse: str
    tokens: list[BaseToken] = []


    def __init__(self, to_parse: str):
        self.to_parse = to_parse
        self.generate_tokens()

    def generate_tokens(self) -> None:
        """Generate the tokens of the given code"""
        tokens: list[BaseToken] = []

        offset = 0
        to_parse = self.to_parse
        offset_limit = len(to_parse)
        while offset < offset_limit:
            token: BaseToken = self.next_word(offset, offset_limit)
            tokens.append(token)
            offset = token.get_offset() + len(token.get_word())
        self.tokens = tokens

    def next_word(self, offset: int, offset_limit: int) -> BaseToken:
        """Return the token of the next word"""
        to_parse = self.to_parse
        start_offset = offset
        i = offset
        word = ""
        end = False
        while i < offset_limit and not end:
            caracter = to_parse[i]
            if caracter == " ":
                if word == "":
                    start_offset += 1
                    i += 1
                else:
                    i -= 1
                    end = True
            elif caracter == "\n" and word == "":
                start_offset += 1
                i += 1
            elif i + 1 < offset_limit and is_comment_start(to_parse[i:i+2]):
                start_offset = get_end_of_comment_index(i, offset_limit, to_parse)
                i = start_offset
            elif is_key_caracter(caracter):
                if word == "":
                    word = caracter
                else:
                    i -= 1
                end = True
            elif caracter == "\"":
                if word == "":
                    parsed_string = parse_string(i, offset_limit, to_parse)
                    word = parsed_string[0]
                    i = parsed_string[1]
                else:
                    i -= 1
                end = True
            else:
                word += caracter
                i += 1
        return BaseToken(start_offset, word)

    def get_tokens(self) -> list[BaseToken]:
        """Return the tokens of the given code"""
        return self.tokens

    def convert_to_asm(self) -> str:
        """Convert the parsed code to assembly code"""
        return ""