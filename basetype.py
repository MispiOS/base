from enum import Enum
from utils import operators, brackets, keywords, types, starts_with_number, is_number
from parserException import ParserException

class BaseType(Enum):
    OPERATOR = 0
    SEMILICON = 1
    EQUAL = 2
    STRING = 3
    NUMBER = 4
    BRACKET = 5
    KEYWORD = 6
    OTHER = 7
    TYPE = 8
    POINTER = 9
    COMMA = 10


def get_base_type(value: str) -> BaseType|ParserException:
    """Return the type of a value"""
    if value == ";":
        res = BaseType.SEMILICON
    elif value == "=":
        res = BaseType.EQUAL
    elif value == "$":
        res = BaseType.POINTER
    elif value == ",":
        res = BaseType.COMMA
    elif value.startswith("\""):
        res = BaseType.STRING
    elif value in operators:
        res = BaseType.OPERATOR
    elif value in brackets:
        res = BaseType.BRACKET
    elif value in keywords:
        res = BaseType.KEYWORD
    elif value in types:
        res = BaseType.TYPE
    else:
        if starts_with_number(value):
            if is_number(value):
                res = BaseType.NUMBER
            else:
                res = ParserException.VARIABLE_FUNCTION_CANNOT_STARTS_WITH_NUMBER
        else:
            res = BaseType.OTHER
    return res
