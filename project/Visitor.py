from Nodes import *
from prettytable import PrettyTable


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

        if type(node) is funcDefSubtree:
            print("visiting funcBodySubtree")
            funcId = node.children[0].data
            funcParmsChildren = node.children[1].children
            funcType = node.children[2].data
            funcBodyChildren = node.children[3].children

            #updating local to param
            funcParams = ()
            for param in funcParmsChildren:
                for var in funcBodyChildren:
                    if var.__class__.__name__ == varDeclSubtree and param.symRecord.list[1] == var.symRecord.list[1]:
                        var.symRecord.list[0] = "param"
                funcParams += (param.symRecord.list[2],)

            # creating table
            funcTable = PrettyTable(title="table: " + funcId, header=False)
            for child in funcBodyChildren:
                if child.__class__.__name__ == "varDeclSubtree":
                    funcTable.add_row(child.symRecord.list)

            node.symRecord = FunctionEntry(funcId, funcType, funcParams, visibility=None, table=funcTable)

            # This should be deleted:
            entryTable = PrettyTable(header=False)
            entryTable.add_row(node.symRecord.list)
            print(entryTable)

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

        if type(node) is progSubtree:
            print("visiting progSubtree")
            structChildren = node.children[0].children
            implChildren = node.children[1].children
            progChildren = node.children[2].children

            node.symTable = PrettyTable(title="table: global", header=False, hrules=True)
            for prog in progChildren:
                node.symTable.add_row(prog.symRecord.list)
            print(node.symTable)


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

        if type(node) is varDeclSubtree:
            print("visiting varDeclSubtree")
            varName = node.children[0].data
            varType = node.children[1].data
            dimListChildren = node.children[2].children
            varDimlist = list()
            for arrSize in dimListChildren:
                if len(arrSize.children) > 0: #[3]
                    varDimlist.append("[" + str(arrSize.children[0].data) + "]")
                else: #[]
                    varDimlist.append("[]")
            entry = Entry("local", varName, varType, varDimlist)
            node.symRecord = entry
            print(entry)

        if type(node) is varSubtree: pass

        if type(node) is visibilityNode: pass

        if type(node) is whileSubtree: pass

        if type(node) is writeSubtree: pass

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
    def __init__(self, category, id, type, dimList="", visibility=""):
        self.category = category
        self.id = id
        self.type = type
        self.dimList = dimList
        self.visibility = visibility
        self.dimStr = ""
        if self.dimList != "":
            for dim in self.dimList:
                self.dimStr += dim
        self.list = [self.category, self.id, str(self.type) + str(self.dimStr)]

    def __str__(self):
        if self.dimList and self.visibility:
            return "%s\t | %s\t | %s%s\t | %s" % (self.category, self.id, self.type, self.dimStr, self.visibility)
        if self.dimList:
            return "%s\t | %s\t | %s%s\t" % (self.category, self.id, self.type, self.dimStr)
        if self.visibility:
            return "%s\t | %s\t | %s\t | %s\t" % (self.category, self.id, self.type, self.visibility)
        else:
            return "%s\t | %s\t | %s\t" % (self.category, self.id, self.type)

class FunctionEntry():
    def __init__(self, id, type, parms, visibility="", table=""):
        self.category = "function"
        self.id = id

        self.type = ""
        if type:
            self.type = type

        self.parms = "()"
        if len(parms) > 0:
            self.parms = str(parms)

        self.parms += ":" + str(self.type)

        self.table = table

        self.visibility = ""
        if visibility:
            self.visibility = visibility


        self.list = [self.category, self.id, self.parms, self.visibility, self.table]

# => funcBodySubtree
# => memberDeclListSubtree
# - name
# - Entry (per variable)
class Table():
    def __init__(self, tableName):
        self.tableName = tableName
        self.table = list()

    def __str__(self):
        pass



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
def Class(self): pas