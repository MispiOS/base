from sys import argv
from filemanager import *
from parser import Parser

if __name__ == "__main__":
    if len(argv) != 2:
        print("No file given in arguments")
        exit(0)
    
    filepath = argv[1]

    if not filepath.endswith(".base"):
        print("The given file is not a Base file")
        exit(0)

    file_content = read_file(filepath)
    
    if file_content == None:
        print("The file given in arguments doesn't exist")
        exit(0)
    
    parser = Parser(file_content)
    
    asm_filepath = filepath[:-4] + ".asm"
    
    write_file(asm_filepath, parser.convert_to_asm())
