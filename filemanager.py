def read_file(filepath: str) -> str|None:
    """Return the content of a given file or None if it doesn't exist"""
    try:
        content = open(filepath, "r").read()
    except:
        content = None
    return content

def write_file(filepath: str, content: str):
    """Write into the file the given content"""
    file = open(filepath, "w")
    file.write(content)
    file.close()