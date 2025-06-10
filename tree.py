from enum import Enum

class NodeType(Enum):
    TREE = 0
    FUNCTION = 1
    CALL = 2
    DEFINITION = 3
    ARITHMETIC = 4
    CONDITION = 5

class Node:
    type: NodeType = None

class BinaryNode(Node):
    left = None
    right = None

    def __init__(self, l=None, r=None):
        if l != None:
            self.left = l
            self.right = r

class BinaryTree(BinaryNode):
    def __init__(self, l=None, r=None):
        super().__init__(l, r)
        self.type = NodeType.TREE
        
    def add(self, data):
        if self.left == None:
            self.left = data
        elif self.right == None:
            self.right = BinaryTree(l=data)
        else:
            self.right.add(data)

class FunctionNode(BinaryNode):
    name: str
    args: list[tuple[str, str]]
    retType: str
    content: BinaryTree

    def __init__(self, name: str, args: list[tuple[str,str]], retType: str, content: BinaryTree):
        self.type = NodeType.FUNCTION
        self.name = name
        self.args = args
        self.retType = retType
        self.content = content

    def get_name(self) -> str:
        return self.name        
    def get_args(self) -> list[tuple[str,str]]:
        return self.args
    def get_type(self) -> str:
        return self.retType
    def get_content(self) -> BinaryTree:
        return self.content
    def __str__(self):
        return f"Name: {self.name}\nArgs: {str(self.args)}\nReturn Type: {self.retType}"

class ValidDefNode(Node):
    def __init__(self):
        super().__init__()

class ArithmeticNode(ValidDefNode, BinaryNode):
    operator: str
    a: ValidDefNode|str
    b: ValidDefNode|str

    def __init__(self, operator: str, a: ValidDefNode|str, b: ValidDefNode|str):
        self.type = NodeType.ARITHMETIC
        self.operator = operator
        self.a = a
        self.b = b
    
    def get_operator(self) -> str:
        return self.operator
    def get_a(self) -> ValidDefNode|str:
        return self.a
    def get_b(self) -> ValidDefNode|str:
        return self.b

class ConditionNode(ValidDefNode, BinaryNode):
    def __init__(self):
        self.type = NodeType.CONDITION

class FunctionCallNode(ValidDefNode):
    called_function: str
    args: list[ValidDefNode|str]
    def __init__(self, function: str, args: list):
        self.type = NodeType.CALL
        self.calledFunction = function
        self.args = args
    
    def get_called_function(self) -> str:
        return self.called_function
    def get_args(self) -> list:
        return self.args

class DefinitionNode(BinaryNode):
    name: str
    type: str
    value: ValidDefNode|str

    def __init__(self, name: str, varType: str, value: ValidDefNode|str):
        self.type = NodeType.DEFINITION
        self.name = name
        self.type = varType
        self.value = value
    
    def get_name(self) -> str:
        return self.name
    def get_type(self) -> str:
        return self.type
    def get_value(self) -> ValidDefNode|str:
        return self.value