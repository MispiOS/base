from basetoken import BaseToken
from basetype import BaseType
from utils import *
from parserException import ParserException, raiseException
from treeizer import to_token_tree

class Parser:
    to_parse: str
    tokens: list[BaseToken] = []


    def __init__(self, to_parse: str):
        self.to_parse = to_parse
        self.generate_tokens()
        self.verify_brackets()
        token_tree = to_token_tree(self.tokens)
        #print(token_tree)

    def generate_tokens(self) -> None:
        """Generate the tokens of the given code"""
        tokens: list[BaseToken] = []

        offset = 0
        to_parse = self.to_parse
        offset_limit = len(to_parse)
        while offset < offset_limit:
            token: BaseToken|None = self.next_word(offset, offset_limit)
            if token == None:
                offset = offset_limit
                continue
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
                start_offset = get_end_of_comment_index(i, offset_limit, to_parse) + 1
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
        return BaseToken(start_offset, word) if word != "" else None

    def get_tokens(self) -> list[BaseToken]:
        """Return the tokens of the given code"""
        return self.tokens

    def verify_brackets(self) -> None:
        """Verifiy if all brackets are open and closed in the right order"""
        stack = []
        for token in self.tokens:
            if token.get_type() != BaseType.BRACKET:
                continue
            bracket = token.get_word()
            if is_close_bracket(bracket):
                raise_exception = True
                if len(stack) != 0 and is_same_brakets_type(bracket, stack.pop()):
                    raise_exception = False
                if raise_exception:
                    raiseException(ParserException.INCORRECT_BRACKETS, fatal=True)
            else:
                stack.append(bracket)
        if len(stack) != 0:
            raiseException(ParserException.INCORRECT_BRACKETS, fatal=True)

    def convert_to_asm(self) -> str:
        """Convert the parsed code to assembly code"""
        return ""