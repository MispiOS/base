operators = ["+", "-", "*", "/", "%", "^", "|", "&", "!"]
comparators = ["=", "<", ">"]
brackets = ["(", ")", "{", "}", "[", "]"]
other_key_caracters = [";", "$"]
keywords = [
    "if", "else", "else-if", "while", "function", "public", "private", "switch", "case", "break", "return", "null", "void", "default","class",
    "interface", "abstract", "extends", "implements", "import"
]
types = ["int", "float", "char"]

def is_key_caracter(caracter: str) -> bool:
    """Return if the caracter is a keyword"""
    return (caracter in other_key_caracters) or (caracter in operators) or (caracter in comparators) or (caracter in brackets)

def is_comment_start(part: str) -> bool:
    """Return if part is a comment start"""
    return part == "//" or part == "/*"

def get_end_of_comment_index(offset: int, offset_limit: int, to_parse: str) -> int:
    """Return the index of the end of the comment"""
    is_inline = to_parse[offset:offset+2] == "//"
    offset += 2
    end = False
    while offset < offset_limit and not end:
        if (is_inline and to_parse[offset] == "\n") or (offset + 1 < offset_limit and to_parse[offset:offset+2] == "*/"):
            end = True
        offset += 1
    return offset

def parse_string(offset: int, offset_limit: int, to_parse: str) -> tuple:
    """Parse a string from a code"""
    offset += 1
    value = "\""
    end = False
    while offset < offset_limit and not end:
        caracter = to_parse[offset]
        if caracter == "\"" and is_non_text_backslash(offset - 1, to_parse):
            end = True
        value += caracter
        offset += 1
    return (value, offset)
            

def is_non_text_backslash(offset: int, to_parse: str) -> bool:
    """Return if the caracter is a valid escape"""
    if 0 <= offset - 1 and to_parse[offset - 1] == "\\":
        res = not(is_non_text_backslash(offset - 1, to_parse))
    else:
        res = True
    return res

def starts_with_number(string: str) -> bool:
    """Return if the string starts with a number"""
    try:
        int(string[0])
        res = True
    except:
        res = False
    return res

def is_number(string: str) -> bool:
    """Return if the string is a number"""
    try:
        float(string)
        res = True
    except:
        res = False
    return res