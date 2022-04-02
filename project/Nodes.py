from anytree import Node



class BaseNode():

    def __init__(self, token=None):
        self.name = ""
        self.data = None
        self.token = token
        self.symTable = None
        self.symRecord = None
        self.tempVarEntries = None
        self.type = None

    # func def overrides accept !
    def accept(self, visitor, table=None):
        if visitor.__class__.__name__ == "SymTableVisitor" or visitor.__class__.__name__ == "TypeCheckingVisitor":
            self.symTable = visitor.globalTable
            if table:
                self.symTable = table
            for child in self.children:
                if self.tempVarEntries:
                    child.tempVarEntries = self.tempVarEntries
                child.symTable = self.symTable
                child.accept(visitor, table)
            visitor.visit(self)

        else:
            visitor.visit(self)


        
# Special Subtrees #

class progSubtree(BaseNode, Node):
    def __init__(self, children=None):
        super(progSubtree, self).__init__()
        self.name = "prog"
        if children:
            self.children = children

        self.structDecList = children[0]
        self.implDefList = children[1]
        self.funcDefList = children[2]


class implDefSubtree(BaseNode, Node):
    def __init__(self, children=None):
        super(implDefSubtree, self).__init__()
        self.name = "implDef"
        if children:
            self.children = children
        self.id = children[0]
        self.funcDefList = []
        for child in children[1:]:
            self.funcDefList.append(child)


class assignSubtree(BaseNode, Node):
    def __init__(self, children=None):
        super(assignSubtree, self).__init__()
        self.name = "assign"
        if children:
            self.children = children
        newChildren = ()
        for child in children:
            if child.name == "id":
                child = varSubtree((child, indiceListSubtree()))
            newChildren += (child,)
        self.children = newChildren


class dotSubtree(BaseNode, Node):
    def __init__(self, children=None):
        super(dotSubtree, self).__init__()
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

class arrSizeSubtree(BaseNode, Node):
    def __init__(self, children=None):
        super(arrSizeSubtree, self).__init__()
        self.name = "arrSize"
        if children:
            self.children = children

class structDecListSubtree(BaseNode, Node):
    def __init__(self, children=None):
        super(structDecListSubtree, self).__init__()
        self.name = "structDecList"
        if children:
            self.children = children

class implDefListSubtree(BaseNode, Node):
    def __init__(self, children=None):
        super(implDefListSubtree, self).__init__()
        self.name = "implDefList"
        if children:
            self.children = children

class funcDefListSubtree(BaseNode, Node):
    def __init__(self, children=None):
        super(funcDefListSubtree, self).__init__()
        self.name = "funcDefList"
        if children:
            self.children = children

class structDecSubtree(BaseNode, Node):
    def __init__(self, children=None):
        super(structDecSubtree, self).__init__()
        self.name = "structDec"
        if children:
            self.children = children

class funcDefSubtree(BaseNode, Node):
    def __init__(self, children=None):
        super(funcDefSubtree, self).__init__()
        self.name = "funcDef"
        self.tempVarEntries = ["first"]
        if children:
            self.children = children


class funcDeclSubtree(BaseNode, Node):
    def __init__(self, children=None):
        super(funcDeclSubtree, self).__init__()
        self.name = "funcDecl"
        if children:
            self.children = children


class varDeclSubtree(BaseNode, Node):
    def __init__(self, children=None):
        super(varDeclSubtree, self).__init__()
        self.name = "varDecl"
        if children:
            self.children = children

class memberDeclSubtree(BaseNode, Node):
    def __init__(self, children=None):
        super(memberDeclSubtree, self).__init__()
        self.name = "memberDecl"
        if children:
            self.children = children

class dimListSubtree(BaseNode, Node):
    def __init__(self, children=None):
        super(dimListSubtree, self).__init__()
        self.name = "dimList"
        if children:
            self.children = children

class inherListSubtree(BaseNode, Node):
    def __init__(self, children=None):
        super(inherListSubtree, self).__init__()
        self.name = "inherList"
        if children:
            self.children = children

class fparmListSubtree(BaseNode, Node):
    def __init__(self, children=None):
        super(fparmListSubtree, self).__init__()
        self.name = "fparmList"
        if children:
            self.children = children

class funcBodySubtree(BaseNode, Node):
    def __init__(self, children=None):
        super(funcBodySubtree, self).__init__()
        self.name = "funcBody"
        if children:
            self.children = children


class indiceListSubtree(BaseNode, Node):
    def __init__(self, children=None):
        super(indiceListSubtree, self).__init__()
        self.name = "indiceList"
        if children:
            self.children = children

class varSubtree(BaseNode, Node):
    def __init__(self, children=None):
        super(varSubtree, self).__init__()
        self.name = "var"
        if children:
            self.children = children


class aParamsSubtree(BaseNode, Node):
    def __init__(self, children=None):
        super(aParamsSubtree, self).__init__()
        self.name = "aParams"
        if children:
            self.children = children

class readSubtree(BaseNode, Node):
    def __init__(self, children=None):
        super(readSubtree, self).__init__()
        self.name = "read"
        if children:
            self.children = children

class funCallSubtree(BaseNode, Node):
    def __init__(self, children=None):
        super(funCallSubtree, self).__init__()
        self.name = "funCall"
        if children:
            self.children = children

class relOpSubtree(BaseNode, Node):
    def __init__(self, children=None):
        super(relOpSubtree, self).__init__()
        self.name = "rel"
        if children:
            self.children = children

class mulOpSubtree(BaseNode, Node):
    def __init__(self, children=None):
        super(mulOpSubtree, self).__init__()
        self.name = "mul"
        if children:
            self.children = children

class factorSubtree(BaseNode, Node):
    def __init__(self, children=None):
        super(factorSubtree, self).__init__()
        self.name = "factor"
        if children:
            self.children = children

class addOpSubtree(BaseNode, Node):
    def __init__(self, children=None):
        super(addOpSubtree, self).__init__()
        self.name = "add"
        if children:
            self.children = children

class writeSubtree(BaseNode, Node):
    def __init__(self, children=None):
        super(writeSubtree, self).__init__()
        self.name = "write"
        if children:
            self.children = children

class returnSubtree(BaseNode, Node):
    def __init__(self, children=None):
        super(returnSubtree, self).__init__()
        self.name = "return"
        if children:
            self.children = children

class relExprSubtree(BaseNode, Node):
    def __init__(self, children=None):
        super(relExprSubtree, self).__init__()
        self.name = "relExpr"
        if children:
            self.children = children

class statSubtree(BaseNode, Node):
    def __init__(self, children=None):
        super(statSubtree, self).__init__()
        self.name = "stat"
        if children:
            self.children = children

class ifThenElseSubtree(BaseNode, Node):
    def __init__(self, children=None):
        super(ifThenElseSubtree, self).__init__()
        self.name = "ifThenElse"
        if children:
            self.children = children

class whileSubtree(BaseNode, Node):
    def __init__(self, children=None):
        super(whileSubtree, self).__init__()
        self.name = "while"
        if children:
            self.children = children
class memberDeclListSubtree(BaseNode, Node):
    def __init__(self, children=None):
        super(memberDeclListSubtree, self).__init__()
        self.name = "memberDeclList"
        if children:
            self.children = children

# Nodes #


class typeNode(BaseNode, Node):
    def __init__(self, token=None, data=None):
        super(typeNode, self).__init__()
        self.name = "type"
        self.token = token
        if token:
            self.data = token.lexeme
        if data:
            self.data = data


class IdNode(BaseNode, Node):
    def __init__(self, token=None, data=None):
        super(IdNode, self).__init__()
        self.name = "id"
        self.token = token
        if token:
            self.data = token.lexeme
        if data:
            self.data = data

class relOpNode(BaseNode, Node):
    def __init__(self, token=None, data=None):
        super(relOpNode, self).__init__()
        self.name = "relOp"
        self.token = token
        if token:
            self.data = token.lexeme
        if data:
            self.data = data

class numNode(BaseNode, Node):
    def __init__(self, token=None, data=None):
        super(numNode, self).__init__()
        self.name = "num"
        self.token = token
        if token:
            self.data = token.lexeme
        if data:
            self.data = data

class floatNode(BaseNode, Node):
    def __init__(self, token=None, data=None):
        super(floatNode, self).__init__()
        self.name = "float"
        self.token = token
        if token:
            self.data = token.lexeme
        if data:
            self.data = data

class visibilityNode(BaseNode, Node):
    def __init__(self, token=None, data=None):
        super(visibilityNode, self).__init__()
        self.name = "visibility"
        self.token = token
        if token:
            self.data = token.lexeme
        if data:
            self.data = data

class signNode(BaseNode, Node):
    def __init__(self, token=None, data=None):
        super(signNode, self).__init__()
        self.name = "sign"
        self.token = token
        if token:
            self.data = token.lexeme
        if data:
            self.data = data

class MulOpNode(BaseNode, Node):
    def __init__(self, token=None, data=None):
        super(MulOpNode, self).__init__()
        self.name = "MulOp"
        self.token = token
        if token:
            self.data = token.lexeme
        if data:
            self.data = data

class addOpNode(BaseNode, Node):
    def __init__(self, token=None, data=None):
        super(addOpNode, self).__init__()
        self.name = "addOp"
        self.token = token
        if token:
            self.data = token.lexeme
        if data:
            self.data = data

