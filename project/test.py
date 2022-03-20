from LexicalAnalyzer import Token
from anytree import Node, RenderTree
from Nodes import *

class Visitor:
    def visit(self, node):

        if type(node) is Node: pass

        if type(node) is IdNode: pass

        if type(node) is MulOpNode: pass

        if type(node) is aParamsSubtree: pass

        if type(node) is addOpNode: pass

        if type(node) is addOpSubtree: pass

        if type(node) is assignSubtree: pass

        if type(node) is dimListSubtree: pass

        if type(node) is dotSubtree: pass

        if type(node) is factorSubtree: pass

        if type(node) is floatNode: pass

        if type(node) is fparmListSubtree: pass

        if type(node) is funCallSubtree: pass

        if type(node) is funcBodySubtree: pass

        if type(node) is funcDeclSubtree: pass

        if type(node) is funcDefListSubtree: pass

        if type(node) is funcDefSubtree: pass

        if type(node) is ifThenElseSubtree: pass

        if type(node) is implDefListSubtree: pass

        if type(node) is implDefSubtree: pass

        if type(node) is indiceListSubtree: pass

        if type(node) is inherListSubtree: pass

        if type(node) is memberDeclListSubtree: pass

        if type(node) is memberDeclSubtree: pass

        if type(node) is mulOpSubtree: pass

        if type(node) is numNode: pass

        if type(node) is progSubtree: pass

        if type(node) is readSubtree: pass

        if type(node) is relExprSubtree: pass

        if type(node) is relOpNode: pass

        if type(node) is relOpSubtree: pass

        if type(node) is returnSubtree: pass

        if type(node) is signNode: pass

        if type(node) is statSubtree: pass

        if type(node) is structDecListSubtree: pass

        if type(node) is structDecSubtree: pass

        if type(node) is typeNode: pass

        if type(node) is varDeclSubtree: pass

        if type(node) is varSubtree: pass

        if type(node) is visibilityNode: pass

        if type(node) is whileSubtree: pass

        if type(node) is writeSubtree: pass

class SymTabCreationVisitor(Visitor):
    if type(node) is varDeclSubtree) -> None:
        for child in e.children:
            child.symList = e.symList
            child.accept(self)
        id = e.children[0].id
        type = e.children[1].type
        dimlist = list()
        for dim in e.children[2]:
            dimlist.append(dim.num)
        varDeclSubtree.symEntry = SymTabEntry("var", type, id, dimlist)


    if type(node) is IdNode) -> None:
        for child in e.children:
            child.symList = e.symList
            child.accept(self)

    if type(node) is typeNode) -> None:
        for child in e.children:
            child.symList = e.symList
            child.accept(self)

class SymbolTable:
    def __init__(self, name):
        self.name = name
        self.symList = list()

    def addEntry(self, entry):
        self.symList.append(entry)

class SymTabEntry:
    def __init__(self, kind, type, name, subTable):
        self.kind = kind
        self.type = type
        self.name = name
        self.subTable = subTable


class BaseNode():
    def __init__(self, token=None):
        self.name = ""
        self.token = token
        self.symList = list()
        self.symEntry = None

    def accept(self, visitor: Visitor) -> None:
        pass


class varDeclSubtree(BaseNode, Node):
    def __init__(self, children=None):
        super(varDeclSubtree, self).__init__()
        self.name = "varDecl"
        if children:
            self.children = children

    def accept(self, visitor: Visitor) -> None:
        visitor.visit(self)


class typeNode(BaseNode, Node):
    def __init__(self, token=None, type=None):
        super(typeNode, self).__init__()
        self.name = "type"
        self.token = token
        if type:
            self.type = type

    def accept(self, visitor: Visitor) -> None:
        visitor.visit(self)


class IdNode(BaseNode, Node):
    def __init__(self, token=None, id=None):
        super(IdNode, self).__init__()
        self.name = "id"
        self.token = token
        if id:
            self.type = id

    def accept(self, visitor: Visitor) -> None:
        visitor.visit(self)


n1 = IdNode(id="x")
n2 = typeNode(type="float")
n3 = varDeclSubtree((n1, n2))



print("PLAN FOR TODAY \n 1) try to make the tables symbTabes witout visitor \n \t "
      "a) create a method Construct in each node that will do the data entry and whatnot \n "
      "2) seperate into visitor \n")

# print(n3.children)
#
# for pre, fill, node in RenderTree(n3):
#     print("%s%s" % (pre, node.name))