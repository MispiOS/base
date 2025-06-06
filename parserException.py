from enum import Enum

class ParserException(Enum):
    NO_FILE_GIVEN = "No file given in arguments"
    NOT_BASE_FILE = "The file '{}' is not a Base file"
    FILE_DOES_NOT_EXISTS = "The file '{}' doesn't exist"
    VARIABLE_FUNCTION_CANNOT_STARTS_WITH_NUMBER = "A variable name or a function name can't start with a number\nAt '{}'."
    INCORRECT_BRACKETS = "Bracket are not correct !"

def raiseExceptionStr(exception: str, fatal: bool = True):
    """Raise an Exception and terminate the program if asked"""
    print(exception)
    if fatal:
        exit(0)

def raiseException(exception: ParserException, *args: str, fatal: bool = True):
    """Raise an Exception, format the text and terminate the program if asked"""
    to_print = exception.value

    for value in args:
        to_print = to_print.replace("{}", value, 1)
    raiseExceptionStr(to_print, fatal)