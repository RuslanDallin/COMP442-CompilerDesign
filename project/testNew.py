from LexicalAnalyzer import Token
from anytree import Node, RenderTree
from Nodes import *

class Visitor():
    def visit(self, node):
        if type(node) is varDeclSubtree:
            varName = node.children[0].data
            varType = node.children[1].data
            varDimlist = list()
            for child in node.children[2].children:
                varDimlist.append(child.data)
            print("=>>",varName,varType,varDimlist)
            entry = Entry("local", varName, varType, varDimlist)
            print(entry)


        if type(node) is typeNode:
            print("visiting typeNode")

        if type(node) is IdNode:
            print("visiting IdNode")

        if type(node) is dimListSubtree:
            print("visiting dimListSubtree")

        if type(node) is numNode:
            print("visiting numNode")

class symbolTable(): pass

#TODO 1) inherList 2) functionList?

# => varDeclSubtree
# => memberDeclListSubtree
# - category:
#       - data if in memberDeclListSubtree
#       - local
#       - param if present in memberDeclListSubtree)
# - name
# - type
# - dimList
# - visibility: private/public (only if memberDeclListSubtree)
class Entry():
    def __init__(self, category, id, type, dimList=None, visibility=None):
        self.category = category
        self.id = id
        self.type = type
        self.dimList = dimList
        if self.dimList:
            self.dimList = ""
            for dim in dimList:
                self.dimList += "[" + str(dim) + "]"
        self.visibility = visibility

    def __str__(self):
        if self.dimList and self.visibility:
            return "%s\t | %s\t | %s%s\t | %s" % (self.category, self.id, self.type, self.dimList, self.visibility)
        if self.dimList:
            return "%s\t | %s\t | %s%s\t" % (self.category, self.id, self.type, self.dimList)
        if self.visibility:
            return "%s\t | %s\t | %s\t | %s\t" % (self.category, self.id, self.type, self.visibility)
        else:
            return "%s\t | %s\t | %s\t" % (self.category, self.id, self.type)

# => funcBodySubtree
# => memberDeclListSubtree
# - name
# - Entry (per variable)
class Table():
    def __init__(self): pass

# => funcDefSubtree
# - name
# - parms (or empty if main)
# - returnType (or empty if main)
# - private/public (only if Class)
# - Table
class Function():
    def __init__(self): pass


# - inheritance list
# - data (data +
# - function(s)
def Class(self): pass


class BaseNode():
    def __init__(self, token=None):
        self.name = ""
        self.token = token
        self.symList = list()
        self.symEntry = None

    def accept(self, visitor):
        for child in self.children:
            print("\tcalling ", child.name, "'s visit")
            child.accept(visitor)
        visitor.visit(self)


class varDeclSubtree(BaseNode, Node):
    def __init__(self, children=None):
        super(varDeclSubtree, self).__init__()
        self.name = "varDecl"
        if children:
            self.children = children

class typeNode(BaseNode, Node):
    def __init__(self, token=None, type=None):
        super(typeNode, self).__init__()
        self.name = "type"
        self.token = token
        if type:
            self.data = type

class IdNode(BaseNode, Node):
    def __init__(self, token=None, id=None):
        super(IdNode, self).__init__()
        self.name = "id"
        self.token = token
        if id:
            self.data = id

class dimListSubtree(BaseNode, Node):
    def __init__(self, children=None):
        super(dimListSubtree, self).__init__()
        self.name = "dimList"
        if children:
            self.children = children

class numNode(BaseNode, Node):
    def __init__(self, token=None, num=None):
        super(numNode, self).__init__()
        self.name = "num"
        self.token = token
        self.data = num
        if num:
            self.data = num


n1 = IdNode(id="x")
n2 = typeNode(type="float")
n31 = numNode(num=3)
n3 = dimListSubtree((n31,))
n4 = varDeclSubtree((n1, n2, n3))




print("PLAN FOR TODAY \n 1) try to make the tables symbTabes witout visitor \n \t "
      "a) create a method Construct in each node that will do the data entry and whatnot \n "
      "2) seperate into visitor \n")

visitor = Visitor()

n4.accept(visitor)

for pre, fill, node in RenderTree(n4):
    print("%s%s" % (pre, node.name))

# en = Entry("local", "n", "integer", visibility="private")
# en = Entry("local", "n", "integer", (2,1))
# en2 = Entry("local", "n", "integer", ())
# print(en)
# print(en2)