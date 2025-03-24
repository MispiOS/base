from sys import argv
from filemanager import *
from parser import Parser
from parserException import *

if __name__ == "__main__":
    if len(argv) != 2:
        raiseException(ParserException.NO_FILE_GIVEN)
    
    filepath = argv[1]

    if not filepath.endswith(".base"):
        raiseException(ParserException.NOT_BASE_FILE, filepath)

    file_content = read_file(filepath)
    
    if file_content == None:
        raiseException(ParserException.FILE_DOES_NOT_EXISTS, filepath)
    
    parser = Parser(file_content)
    
    asm_filepath = filepath[:-4] + ".asm"
    
    write_file(asm_filepath, parser.convert_to_asm())
