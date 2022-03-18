from LexicalAnalyzer import Token
from anytree import Node, RenderTree
from Nodes import *

class Visitor():
    def visit(self, node):
        if type(node) is varDeclSubtree:
            print("visiting varDeclSubtree")
        if type(node) is typeNode:
            print("visiting typeNode")
        if type(node) is IdNode:
            print("visiting IdNode")

class symbolTable():

    # => varDeclSubtree
    # => memberDeclListSubtree
    # - local/param (param if present in memberDeclListSubtree)
    # - name
    # - type
    # - dimList
    # - private/public (only if memberDeclListSubtree)
    def addEntry(self, category, id, type):
        if category == None:
            self.cate

    # => funcBodySubtree
    # => memberDeclListSubtree
    # - name
    # - Entry (per variable)
    def addTable(self): pass

    # => funcDefSubtree
    # - name
    # - parms (or empty if main)
    # - returnType (or empty if main)
    # - private/public (only if Class)
    # - Table
    def addFunction(self): pass


    # - inheritance list
    # - data (data +
    # - function(s)
    def addClass(self): pass


class BaseNode():
    def __init__(self, token=None):
        self.name = ""
        self.token = token
        self.symList = list()
        self.symEntry = None

    def accept(self, visitor):
        visitor.visit(self)


class varDeclSubtree(BaseNode, Node):
    def __init__(self, children=None):
        super(varDeclSubtree, self).__init__()
        self.name = "varDecl"
        if children:
            self.children = children

    def accept(self, visitor):
        for child in self.children:
            print("calling ", child.name, "'s visit")
            child.accept(visitor)
        print("called ", self.name, "'s visit")
        visitor.visit(self)


class typeNode(BaseNode, Node):
    def __init__(self, token=None, type=None):
        super(typeNode, self).__init__()
        self.name = "type"
        self.token = token
        if type:
            self.type = type

    def accept(self, visitor):
        print("called ", self.name, "'s visit")
        visitor.visit(self)


class IdNode(BaseNode, Node):
    def __init__(self, token=None, id=None):
        super(IdNode, self).__init__()
        self.name = "id"
        self.token = token
        if id:
            self.type = id

    def accept(self, visitor):
        print("called ", self.name, "'s visit")
        visitor.visit(self)


n1 = IdNode(id="x")
n2 = typeNode(type="float")
n3 = varDeclSubtree((n1, n2))



print("PLAN FOR TODAY \n 1) try to make the tables symbTabes witout visitor \n \t "
      "a) create a method Construct in each node that will do the data entry and whatnot \n "
      "2) seperate into visitor \n")

visitor = Visitor()

print(n3.accept(visitor))

for pre, fill, node in RenderTree(n3):
    print("%s%s" % (pre, node.name))