from basetype import BaseType, get_base_type
from parserException import raiseException

class BaseToken:
    offset: int
    word: str
    token_type: BaseType

    def __init__(self, offset: int, word: str): # ajouter ligne
        self.offset = offset
        self.word = word
        token_type = get_base_type(word)

        if type(token_type) == BaseType:
            self.token_type = token_type
        else:
            raiseException(token_type, word, fatal=True)

    def get_offset(self) -> int:
        """Return the Token's offset"""
        return self.offset

    def get_word(self) -> str:
        """Return the Token's word"""
        return self.word
    
    def get_type(self) -> BaseType:
        """Return the Token's word type"""
        return self.token_type