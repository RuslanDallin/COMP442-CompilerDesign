from Nodes import *
from prettytable import PrettyTable


class Visitor:
    def createGlobalTable(self):
        return PrettyTable(title="table: global", header=False, hrules=True)

    def visit(self, node):

        if type(node) is progSubtree:
            print("visiting progSubtree")
            structChildren = node.children[0].children
            implChildren = node.children[1].children
            progChildren = node.children[2].children

            for prog in progChildren:
                node.symTable.add_row(prog.symRecord.list)
            print(node.symTable)

            # 1st index is row (0-n)
            # second index is the col
            # this fetches i in the printArray table
            # print(node.symTable.rows[1][4].rows[1][1])


        if type(node) is structDecSubtree:
            print("visiting structDecSubtree")
            classtId = node.children[0].data
            inherChildren = node.children[1].children
            memberDecChildren = node.children[2].children

            classTable = PrettyTable(title="class: " + classtId, header=False, hrules=True)

            inherList = ()
            for child in inherChildren:
                inherList += (child.data,)

            classTable.add_row(["inherits: " + str(inherList)])

            print("here3", classTable)

            #placing var data members in data table
            dataTable = PrettyTable(title="data", header=False)
            for member in memberDecChildren:
                if member.symRecord[0] != "function":
                    dataTable.add_row(member.symRecord)

            classTable.add_row([dataTable])


            for member in memberDecChildren:
                if member.symRecord[0] == "function":
                    funcTable = PrettyTable(title="table: " + str(classtId) + "::" + str(member.symRecord[1]), header=False)
                    funcTable.add_row(member.symRecord)
                    classTable.add_row([funcTable])


            print("here4",classTable)







        if type(node) is funcDefSubtree:
            print("visiting funcBodySubtree")
            funcId = node.children[0].data
            funcParmsChildren = node.children[1].children
            funcType = node.children[2].data
            funcBodyChildren = node.children[3].children

            #updating local to param
            funcParams = ()
            for param in funcParmsChildren:
                if param.__class__.__name__ == "varDeclSubtree":
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

        if type(node) is memberDeclSubtree:
            print("visiting memberDeclSubtree")
            visibility = node.children[0].data
            if node.children[1].__class__.__name__ == "varDeclSubtree":
                varRecord = node.children[1].symRecord.list
                varRecord.append(visibility)
                varRecord[0] = "data"
                node.symRecord = varRecord
            if node.children[1].__class__.__name__ == "funcDeclSubtree":
                funcRecord = node.children[1].symRecord.list
                funcRecord[3] = visibility
                node.symRecord = funcRecord

                #TODO need to move fparm from funcDec to it's own method to avoid rewriting the code

        if type(node) is funcDeclSubtree:
            print("visiting funcDeclSubtree")
            funcId = node.children[0].data
            funcParmsChildren = node.children[1].children
            funcType = node.children[2].data


            #updating local to param
            funcParams = ()
            funcTable = PrettyTable(title="table: " + funcId, header=False)
            for param in funcParmsChildren:
                if param.__class__.__name__ == "varDeclSubtree":
                    param.symRecord.list[0] = "param"
                    funcParams += (param.symRecord.list[2],)
                    funcTable.add_row(param.symRecord.list)

            node.symRecord = FunctionEntry(funcId, funcType, funcParams, visibility=None, table=funcTable)
            print("here6", node.symRecord.table)

            # # creating table
            # funcTable = PrettyTable(title="table: " + funcId, header=False)
            # for child in funcBodyChildren:
            #     if child.__class__.__name__ == "varDeclSubtree":
            #         print(child.symRecord.list)
            #         funcTable.add_row(child.symRecord.list)
            #
            # node.symRecord = FunctionEntry(funcId, funcType, funcParams, visibility=None, table=funcTable)
            #
            # # This should be deleted:
            # entryTable = PrettyTable(header=False)
            # entryTable.add_row(node.symRecord.list)
            # print(entryTable)

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
            entry = Entry(varName, varType, varDimlist)
            node.symRecord = entry
            print(entry)

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

        if type(node) is funcDefListSubtree: pass

        if type(node) is funcDefSubtree: pass

        if type(node) is ifThenElseSubtree: pass

        if type(node) is implDefListSubtree: pass

        if type(node) is implDefSubtree: pass

        if type(node) is indiceListSubtree: pass

        if type(node) is inherListSubtree: pass

        if type(node) is memberDeclListSubtree: pass



        if type(node) is mulOpSubtree: pass

        if type(node) is numNode: pass



        if type(node) is readSubtree: pass

        if type(node) is relExprSubtree: pass

        if type(node) is relOpNode: pass

        if type(node) is relOpSubtree: pass

        if type(node) is returnSubtree: pass

        if type(node) is signNode: pass

        if type(node) is statSubtree: pass

        if type(node) is structDecListSubtree: pass

        if type(node) is typeNode: pass



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
    def __init__(self, id, type, dimList="", visibility=""):
        self.category = "local"
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

class memberDataEntry():
    def __init__(self, dataEntry, visibility):
        self.visibility = visibility
        self.list = dataEntry.append(self.visibility)

    def __str__(self):
        return "%s\t | %s" % (self.list, self.visibility)



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


class ClassEntry():
    def __init__(self, id, inherList, dataMembeEntries, funcEntries):
        self.category = "class"
        self.id = id
        self.inherList = inherList
        self.dataMembeEntries = dataMembeEntries

        table = PrettyTable(title="Class: " + str(self.id), header=False)
        table.add_row("inherit", inherList, "", "")

        for data in dataMembeEntries:
            table.add_row(data)



        self.functionTableList = list()
        for func in funcEntries:
            self.functionTableList.append(PrettyTable(title="Function: " + str(self.id) + str(func[1]), header=False))








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
def Class(self): pass

