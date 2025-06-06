from basetoken import BaseToken
from basetype import BaseType
from parserException import ParserException, raiseException
from utils import types, types_size, is_close_bracket, is_same_brakets_type

def to_token_tree(tokens: list[BaseToken], inside_function=False) -> list:
    """Transform tokens list to a tree"""
    tree = []
    i = 0
    while i < len(tokens):
        actual_token = tokens[i]
        token_type = actual_token.get_type()
        token_value = actual_token.get_word()
        if token_type == BaseType.KEYWORD:
            if token_value == "function":
                fnct_tree = function_tree(tokens, i)
                tree.append( fnct_tree[1] )
                i = fnct_tree[0]
        else:
            i += 1
    return tree

def function_tree(tokens: list[BaseToken], start: int) -> tuple[int, dict]:
    """Transform tokens to a function tree
    Returns the index of end of the function (after the '}') and the tree"""
    if start + 3 >= len(tokens):
        raiseException(ParserException.INVALID_FILE)
    
    type_token = tokens[start + 1]
    function_name_token = tokens[start + 2]

    if(
        function_name_token.get_type() == BaseType.OTHER and
        (
            (
                type_token.get_type() == BaseType.TYPE and
                type_token.get_word() in types
            ) or
            type_token.get_type() == BaseType.OTHER
        )
    ):
        open_arg_bracket_token = tokens[start + 3]
        if open_arg_bracket_token.get_word() != "(":
            raiseException(ParserException.UNEXPECTED_WORD, open_arg_bracket_token.get_word(), fatal=True)
        i = start + 4
        not_formated_args: list[BaseToken] = []
        last_type = BaseType.BRACKET
        stop = False
        while i < len(tokens) and not stop:
            actual_token = tokens[i]
            actual_token_type = actual_token.get_type()
            if actual_token_type == BaseType.BRACKET:
                if actual_token.get_word() == ")":
                    stop = True
                else:
                    raiseException(ParserException.UNEXPECTED_WORD_EXPECT, actual_token.get_word(), ")", fatal=True)
            elif actual_token_type == BaseType.TYPE:
                if not last_type in [BaseType.BRACKET, BaseType.COMMA]:
                    raiseException(ParserException.UNEXPECTED_WORD, actual_token.get_word(), fatal=True)
                last_type = BaseType.TYPE
                not_formated_args.append(actual_token)
            elif actual_token_type == BaseType.OTHER:
                if not last_type == BaseType.TYPE and actual_token.get_word() == "void":
                    raiseException(ParserException.UNEXPECTED_WORD, actual_token.get_word(), fatal=True)
                last_type = BaseType.OTHER
                not_formated_args.append(actual_token)
            elif actual_token_type == BaseType.COMMA:
                if not last_type == BaseType.OTHER:
                    raiseException(ParserException.UNEXPECTED_WORD, actual_token.get_word(), fatal=True)
                last_type = BaseType.COMMA
            else:
                raiseException(ParserException.INVALID_FILE, fatal=True)
            i += 1
        if not stop or len(not_formated_args) % 2 != 0:
            raiseException(ParserException.INVALID_FILE, fatal=True)
        
        formated_args = []
        for j in range(len(not_formated_args) // 2):
            arg_type = not_formated_args[j * 2].get_word()
            arg_name = not_formated_args[j * 2 + 1].get_word()
            size = types_size[arg_type]
            formated_args.append(
                {
                    "size": size,
                    "name": arg_name,
                    "type": arg_type
                }
            )
        
        open_function_bracket_token = tokens[i]
        if not open_function_bracket_token.get_word() == "{":
            raiseException(ParserException.UNEXPECTED_WORD_EXPECT, open_function_bracket_token.get_word(), "{")
        
        i += 1
        function_start = i
        stop = False
        stack = []
        while i < len(tokens) and not stop:
            actual_token = tokens[i]
            if actual_token.get_type() == BaseType.BRACKET:
                if not is_close_bracket(actual_token.get_word()):
                    continue
                if len(stack) == 0:
                    if actual_token.get_word() == "}":
                        stop = True
                        continue
                    else:
                        raiseException(ParserException.UNEXPECTED_WORD, actual_token.get_word(), fatal=True)
                previous_bracket = stack.pop()
                if not is_same_brakets_type(previous_bracket, actual_token.get_word()):
                    raiseException(ParserException.INCORRECT_BRACKETS, fatal=True)
            i += 1
        
        content = to_token_tree(tokens[function_start:i], inside_function=True)

        return (i, {
            "type": "function",
            "name": function_name_token.get_word(),
            "args": formated_args,
            "content": content
        })
    else:
        raiseException(ParserException.UNEXPECTED_WORD, "function", fatal=True)
    return None