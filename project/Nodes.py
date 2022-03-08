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

class implDefSubtree(Node):
    def __init__(self, children=None):
        self.name = "implDef"
        if children:
            self.children = children
        self.id = children[0]
        self.funcDefList = []
        for child in children[1:]:
            self.funcDefList.append(child)


class funcDefSubtree(Node):
    def __init__(self, children=None):
        self.name = "funcDef"
        if children:
            self.children = children


class varDeclSubtree(Node):
    def __init__(self, children=None):
         self.name = "varDecl"
         if children:
             self.children = children
         self.id = children[0]
         self.type = children[1]
         self.arraySizeList = []
         for child in children[2:]:
             self.arraySizeList.append(child)

class typeNode(Node):
    def __init__(self, token, type=None):
         self.name = "type"
         self.token = token
         self.type = type


class idNode(Node):
    def __init__(self, token, id=None):
        self.name = "id"
        self.token = token
        self.id = id


class numNode(Node):
    def __init__(self, int):
        self.name = "num"
        self.int = int


class arraySizeSubtree(Node):
    def __init__(self, *nums):
        self.name = "arraySize"
        if nums:
            self.children = nums



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
