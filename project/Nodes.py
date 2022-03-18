from anytree import Node

# Special Subtrees #

class progSubtree(Node):
    def __init__(self, children=None):
        self.name = "prog"
        if children:
            self.children = children

        self.structDecList = children[0]
        self.implDefList = children[1]
        self.funcDefList = children[2]


class implDefSubtree(Node):
    def __init__(self, children=None):
        self.name = "implDef"
        if children:
            self.children = children
        self.id = children[0]
        self.funcDefList = []
        for child in children[1:]:
            self.funcDefList.append(child)


class assignSubtree(Node):
    def __init__(self, children=None):
        self.name = "assign"
        if children:
            self.children = children
        newChildren = ()
        for child in children:
            if child.name == "id":
                child = varSubtree((child, indiceListSubtree()))
            newChildren += (child,)
        self.children = newChildren


class dotSubtree(Node):
    def __init__(self, children=None):
        self.name = "dot"
        if children:
            self.children = children
        newChildren = ()
        for child in children:
            if child.name == "id":
                child = varSubtree((child, indiceListSubtree()))
            newChildren += (child,)
        self.children = newChildren

# Subtrees #

class structDecListSubtree(Node):
    def __init__(self, children=None):
        self.name = "structDecList"
        if children:
            self.children = children

class implDefListSubtree(Node):
    def __init__(self, children=None):
        self.name = "implDefList"
        if children:
            self.children = children

class funcDefListSubtree(Node):
    def __init__(self, children=None):
        self.name = "funcDefList"
        if children:
            self.children = children

class structDecSubtree(Node):
    def __init__(self, children=None):
        self.name = "structDec"
        if children:
            self.children = children

class funcDefSubtree(Node):
    def __init__(self, children=None):
        self.name = "funcDef"
        if children:
            self.children = children

class funcDeclSubtree(Node):
    def __init__(self, children=None):
        self.name = "funcDecl"
        if children:
            self.children = children


class varDeclSubtree(Node):
    def __init__(self, children=None):
        self.name = "varDecl"
        if children:
            self.children = children

class memberDeclSubtree(Node):
    def __init__(self, children=None):
        self.name = "memberDecl"
        if children:
            self.children = children

class arraySizeSubtree(Node):
    def __init__(self, *nums):
        self.name = "arraySize"
        if nums:
            self.children = nums

class dimListSubtree(Node):
    def __init__(self, children=None):
        self.name = "dimList"
        if children:
            self.children = children

class inherListSubtree(Node):
    def __init__(self, children=None):
        self.name = "inherList"
        if children:
            self.children = children

class fparmListSubtree(Node):
    def __init__(self, children=None):
        self.name = "fparmList"
        if children:
            self.children = children

class funcBodySubtree(Node):
    def __init__(self, children=None):
        self.name = "funcBody"
        if children:
            self.children = children


class indiceListSubtree(Node):
    def __init__(self, children=None):
        self.name = "indiceList"
        if children:
            self.children = children

class varSubtree(Node):
    def __init__(self, children=None):
        self.name = "var"
        if children:
            self.children = children


class aParamsSubtree(Node):
    def __init__(self, children=None):
        self.name = "aParams"
        if children:
            self.children = children

class readSubtree(Node):
    def __init__(self, children=None):
        self.name = "read"
        if children:
            self.children = children

class funCallSubtree(Node):
    def __init__(self, children=None):
        self.name = "funCall"
        if children:
            self.children = children

class relOpSubtree(Node):
    def __init__(self, children=None):
        self.name = "rel"
        if children:
            self.children = children

class mulOpSubtree(Node):
    def __init__(self, children=None):
        self.name = "mul"
        if children:
            self.children = children

class factorSubtree(Node):
    def __init__(self, children=None):
        self.name = "factor"
        if children:
            self.children = children

class addOpSubtree(Node):
    def __init__(self, children=None):
        self.name = "add"
        if children:
            self.children = children

class writeSubtree(Node):
    def __init__(self, children=None):
        self.name = "write"
        if children:
            self.children = children

class returnSubtree(Node):
    def __init__(self, children=None):
        self.name = "return"
        if children:
            self.children = children

class relExprSubtree(Node):
    def __init__(self, children=None):
        self.name = "relExpr"
        if children:
            self.children = children

class statSubtree(Node):
    def __init__(self, children=None):
        self.name = "stat"
        if children:
            self.children = children

class ifThenElseSubtree(Node):
    def __init__(self, children=None):
        self.name = "ifThenElse"
        if children:
            self.children = children

class whileSubtree(Node):
    def __init__(self, children=None):
        self.name = "while"
        if children:
            self.children = children
class memberDeclListSubtree(Node):
    def __init__(self, children=None):
        self.name = "memberDeclList"
        if children:
            self.children = children

# Nodes #


class typeNode(Node):
    def __init__(self, token, type=None):
        self.name = "type"
        self.token = token
        self.type = token.lexeme
        if type:
            self.type = type


class IdNode(Node):
    def __init__(self, token, id=None):
        self.name = "id"
        self.token = token
        self.id = token.lexeme
        if id:
            self.type = id

class relOpNode(Node):
    def __init__(self, token, relOp=None):
        self.name = "relOp"
        self.token = token
        self.relOp = token.lexeme
        if relOp:
            self.relOp = relOp

class numNode(Node):
    def __init__(self, token, num=None):
        self.name = "num"
        self.token = token
        self.num = token.lexeme
        if num:
            self.num = num

class floatNode(Node):
    def __init__(self, token, float=None):
        self.name = "float"
        self.token = token
        self.float = token.lexeme
        if float:
            self.float = float

class visibilityNode(Node):
    def __init__(self, token, visibility=None):
        self.name = "visibility"
        self.token = token
        self.visibility = token.lexeme
        if visibility:
            self.visibility = visibility

class signNode(Node):
    def __init__(self, token, sign=None):
        self.name = "sign"
        self.token = token
        self.sign = token.lexeme
        if sign:
            self.sign = sign

class MulOpNode(Node):
    def __init__(self, token, MulOp=None):
        self.name = "MulOp"
        self.token = token
        self.MulOp = token.lexeme
        if MulOp:
            self.sign = MulOp

class addOpNode(Node):
    def __init__(self, token, addOp=None):
        self.name = "addOp"
        self.token = token
        self.visibility = token.lexeme
        if addOp:
            self.addOp = addOp

