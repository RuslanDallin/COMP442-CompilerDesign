from anytree import Node, RenderTree
import test

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

method_to_call = getattr(test, 'myNode')
my0 = method_to_call('my0', 0, 0)
print(my0)

class progNode(Node):
    def __init__(self, *args):
        self.name = "prog"

        if args:
            self.children = args

class implDefNode(Node):
    def __init__(self, id, funcDef=None):
        self.name = "implDef"
        self.id = id
        self.children = (id,)

        if funcDef:
            self.funcDef = funcDef
            self.children += (funcDef,)


class varDeclNode(Node):
    def __init__(self, type, id, dimList=None):
         self.name = "varDecl"

         self.type = type
         self.id = id
         self.children = type, id

         if dimList:
             self.dimList = dimList
             self.children += (dimList,)

    def __str__(self):
        return "[%s, %s, %s]" % (self.name, self.type, self.id)

class typeNode(Node):
    def __init__(self, type):
         self.name = "type"
         self.type = type

    def __str__(self):
        return "%s" % (self.type)

class idNode(Node):
    def __init__(self, id):
        self.name = "id"
        self.id = id

    def __str__(self):
        return "%s" % (self.id)

class arraySizeNode(Node):
    def __init__(self, *nums):
        self.name = "arraySize"
        if nums:
            self.children = nums

    def __str__(self):
        return "[%s]" % (self.name)

class numNode(Node):
    def __init__(self, int):
        self.name = "num"
        self.int = int

    def __str__(self):
        return "%s" % (self.int)
#
#
# idTest = idNode("POLYNOMIAL")
# test = implDefNode(idTest)
# idTest1 = idNode("testing")
#
# tempy = (test,idTest1)
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
