from anytree import Node, RenderTree
from LexicalAnalyzer import Token

# class progNode(Node):
#     def __init__(self, structDecl=None, implDef=None, funcDef=None):
#         self.name = "prog"
#
#         self.children = []
#         if structDecl:
#             self.structDecl = structDecl
#             self.children += (structDecl,)
#
#         if implDef:
#             self.implDef = implDef
#             self.children += (implDef,)
#
#         if funcDef:
#             self.funcDef = funcDef
#             self.children += (funcDef,)
#

# my0 = getattr(test, 'myNode')('my0', 0, 0)
# print(my0)

class progSubtree(Node):
    def __init__(self, children=None):
        self.name = "prog"
        if children:
            self.children = children

        self.structDecList = children[0]
        self.implDefList = children[1]
        self.funcDefList = children[2]



class structDecListSubtree(Node):
    def __init__(self, children=None):
        self.name = "structDecList"
        if children:
            self.children = children

        print(children)

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

class implDefSubtree(Node):
    def __init__(self, children=None):
        self.name = "implDef"
        if children:
            self.children = children
        self.id = children[0]
        self.funcDefList = []
        for child in children[1:]:
            self.funcDefList.append(child)

class funcDefListSubtree(Node):
    def __init__(self, children=None):
        self.name = "funcDefList"
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

# class varDeclSubtree(Node):
#     def __init__(self, children=None):
#          self.name = "varDecl"
#          if children:
#              self.children = children
#          self.id = children[0]
#          self.type = children[1]
#          self.arraySizeList = []
#          for child in children[2:]:
#              self.arraySizeList.append(child)

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
        self.name = "fparmList"
        if children:
            self.children = children

class typeNode(Node):
    def __init__(self, token, type=None):
        self.name = "type"
        self.token = token
        self.type = token.lexeme


class idNode(Node):
    def __init__(self, token, id=None):
        self.name = "id"
        self.token = token
        self.id = token.lexeme


class numNode(Node):
    def __init__(self, token, num=None):
        self.name = "num"
        self.token = token
        self.num = token.lexeme


class visibilityNode(Node):
    def __init__(self, token, visibility=None):
        self.name = "visibility"
        self.token = token
        self.visibility = token.lexeme

#
# idTest = idNode("POLYNOMIAL")
# test = implDefNode(idTest)
# idTest1 = idNode("testing")
#
# tempy = ()
# tempy += (test,)
# tempy += (idTest1,)
# prog1 = progNode(*tempy)
#
# print("")
#
# for pre, fill, node in RenderTree(prog1):
#     print("%s%s" % (pre, node.name))
#
# print("")
#
# stack = []
# type = typeNode("V")
# id = idNode("int")
#
# stack.append(type)
# stack.append(id)
# varDecl = varDeclNode(stack.pop(), stack.pop())
#
# for pre, fill, node in RenderTree(varDecl):
#     print("%s%s" % (pre, node))
#
# print("")
#
#
# int = numNode(2)
# int2 = numNode(3)
# arraySize = arraySizeNode(int, int2)
#
# for pre, fill, node in RenderTree(arraySize):
#     print("%s%s" % (pre, node))
#
# print("")
#
# type = typeNode("V")
# id = idNode("int")
#
# int = numNode(2)
# int2 = numNode(3)
# arraySize = arraySizeNode(int,int2)
#
# varDeclNode2 = varDeclNode(type, id, arraySize)
#
# for pre, fill, node in RenderTree(varDeclNode2):
#     print("%s%s" % (pre, node.name))
#
#
#
#
#
#
#
#
#
# class progNode(Node):  # Add Node feature
#     def __init__(self, dimList=None, parent=None, children=None):
#         self.name = "varDecl"
#         if children:
#             self.children = children
#         self.type = children[1]
#         self.id = children[0]
#         self.dimList = dimList
#         self.parent = parent
#
#     def __str__(self):
#         return "[%s, %s]" % (self.name, self.parent)
#
# c = Node("ClassList")
#
# PROG = Node("PROG")
# Assign = Node("Assign", parent=PROG)
# var = Node("var", parent=Assign)
# exp = Node("exp", parent=Assign)
#
#
# for pre, fill, node in RenderTree(PROG):
#     print("%s%s" % (pre, node.name))
#
# print("")
#
