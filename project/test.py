from LexicalAnalyzer import Token
from anytree import Node, RenderTree
from Nodes import *


class Visitor:
    def visit(self, e: Node) -> None: pass

    def visit(self, e: IdNode) -> None: pass

    def visit(self, e: MulOpNode) -> None: pass

    def visit(self, e: aParamsSubtree) -> None: pass

    def visit(self, e: addOpNode) -> None: pass

    def visit(self, e: addOpSubtree) -> None: pass

    def visit(self, e: arraySizeSubtree) -> None: pass

    def visit(self, e: assignSubtree) -> None: pass

    def visit(self, e: dimListSubtree) -> None: pass

    def visit(self, e: dotSubtree) -> None: pass

    def visit(self, e: factorSubtree) -> None: pass

    def visit(self, e: floatNode) -> None: pass

    def visit(self, e: fparmListSubtree) -> None: pass

    def visit(self, e: funCallSubtree) -> None: pass

    def visit(self, e: funcBodySubtree) -> None: pass

    def visit(self, e: funcDeclSubtree) -> None: pass

    def visit(self, e: funcDefListSubtree) -> None: pass

    def visit(self, e: funcDefSubtree) -> None: pass

    def visit(self, e: ifThenElseSubtree) -> None: pass

    def visit(self, e: implDefListSubtree) -> None: pass

    def visit(self, e: implDefSubtree) -> None: pass

    def visit(self, e: indiceListSubtree) -> None: pass

    def visit(self, e: inherListSubtree) -> None: pass

    def visit(self, e: memberDeclListSubtree) -> None: pass

    def visit(self, e: memberDeclSubtree) -> None: pass

    def visit(self, e: mulOpSubtree) -> None: pass

    def visit(self, e: numNode) -> None: pass

    def visit(self, e: progSubtree) -> None: pass

    def visit(self, e: readSubtree) -> None: pass

    def visit(self, e: relExprSubtree) -> None: pass

    def visit(self, e: relOpNode) -> None: pass

    def visit(self, e: relOpSubtree) -> None: pass

    def visit(self, e: returnSubtree) -> None: pass

    def visit(self, e: signNode) -> None: pass

    def visit(self, e: statSubtree) -> None: pass

    def visit(self, e: structDecListSubtree) -> None: pass

    def visit(self, e: structDecSubtree) -> None: pass

    def visit(self, e: typeNode) -> None: pass

    def visit(self, e: varDeclSubtree) -> None: pass

    def visit(self, e: varSubtree) -> None: pass

    def visit(self, e: visibilityNode) -> None: pass

    def visit(self, e: whileSubtree) -> None: pass

    def visit(self, e: writeSubtree) -> None: pass

class SymTabCreationVisitor(Visitor):
    def visit(self, e: varDeclSubtree) -> None:
        for child in e.children:
            child.symList = e.symList
            child.accept(self)
        id = e.children[0].id
        type = e.children[1].type
        dimlist = list()
        for dim in e.children[2]:
            dimlist.append(dim.num)
        varDeclSubtree.symEntry = SymTabEntry("var", type, id, dimlist)


    def visit(self, e: IdNode) -> None:
        for child in e.children:
            child.symList = e.symList
            child.accept(self)

    def visit(self, e: typeNode) -> None:
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