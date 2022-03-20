from LexicalAnalyzer import Token
from anytree import Node, RenderTree
from Nodes import *
from prettytable import PrettyTable

class Visitor():
    def visit(self, node):
        if type(node) is varDeclSubtree:
            print("visiting varDeclSubtree")
            varName = node.children[0].data
            varType = node.children[1].data
            varDimlist = list()
            for child in node.children[2].children:
                varDimlist.append(child.data)
            entry = Entry("local", varName, varType, varDimlist)
            node.symRecord = entry


        if type(node) is funcBodySubtree:
            print("visiting funcBodySubtree")
            # node.symTable = PrettyTable(header=False)
            # for child in node.children:
            #     node.symTable.add_row(child.symRecord.list)
            # print(node.symTable)


        if type(node) is fparmListSubtree:
            print("visiting fparmListSubtree")

        # if type(node) is funcDefSubtree:
        #     print("visiting funcBodySubtree")
        #     funcId = node.children[0].data
        #     funcParms = node.children[1]
        #     funcType = node.children[2].data
        #     node.symTable = PrettyTable(title="table: " + funcId, header=False)
        #     for child in node.children[3].children:
        #         node.symTable.add_row(child.symRecord.list)
        #     print(node.symTable)

        if type(node) is funcDefSubtree:
            print("visiting funcBodySubtree")
            funcId = node.children[0].data
            funcParmsChildren = node.children[1].children
            funcType = node.children[2].data
            funcBodyChildren = node.children[3].children

            funcParams = ()
            for param in funcParmsChildren:
                for var in funcBodyChildren:
                    if param.symRecord.list[1] == var.symRecord.list[1]:
                        var.symRecord.list[0] = "param"
                funcParams += (param.symRecord.list[2],)

            funcTable = PrettyTable(title="table: " + funcId, header=False)
            for child in funcBodyChildren:
                funcTable.add_row(child.symRecord.list)

            node.symRecord = FunctionEntry(funcId, funcType, funcParams, visibility=None, table=funcTable)

            #This should be deleted:
            entryTable = PrettyTable(header=False)
            entryTable.add_row(node.symRecord.list)
            print(entryTable)



        if type(node) is typeNode:
            print("visiting typeNode")

        if type(node) is IdNode:
            print("visiting IdNode")

        if type(node) is dimListSubtree:
            print("visiting dimListSubtree")

        if type(node) is numNode:
            print("visiting numNode")

class symbolTable(): pass




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
        if self.dimList != "":
            self.dimList = ""
            for dim in dimList:
                self.dimList += "[" + str(dim) + "]"
        self.list = [self.category, self.id, str(self.type) + str(self.dimList)]

    def __str__(self):
        if self.dimList and self.visibility:
            return "%s\t | %s\t | %s%s\t | %s" % (self.category, self.id, self.type, self.dimList, self.visibility)
        if self.dimList:
            return "%s\t | %s\t | %s%s\t" % (self.category, self.id, self.type, self.dimList)
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
            self.parms = str(parms) + ":" + str(self.type)

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
def Class(self): pass


n1 = IdNode(data="n")
n2 = typeNode(data="integer")
n31 = numNode(data=3)
n3 = dimListSubtree((n31,))
n4 = varDeclSubtree((n1, n2, n3))

n11 = IdNode(data="i")
n22 = typeNode(data="float")
n33 = dimListSubtree()
n44 = varDeclSubtree((n11, n22, n33))

funcBody = funcBodySubtree((n4,n44))


par1 = IdNode(data="n")
par2 = typeNode(data="integer")
par3 = numNode(data=7)
par4 = dimListSubtree((par3,))
par5 = varDeclSubtree((par1, par2, par4))

par11 = IdNode(data="size")
par22 = typeNode(data="integer")
par44 = dimListSubtree()
par55 = varDeclSubtree((par11, par22, par44))

funcParms = fparmListSubtree((par5, par55,))
returnType = typeNode(data="void")
funcName = IdNode(data="bubbleSort")
func = funcDefSubtree((funcName, funcParms, returnType, funcBody))

for pre, fill, node in RenderTree(func):
    if node.__class__.__name__.endswith("Node"):
        print("%s%s: %s" % (pre, node.name, node.data))
    else:
        print("%s%s" % (pre, node.name))

visitor = Visitor()
func.accept(visitor)


par44 = dimListSubtree()
print(par44.children)

# en1 = Entry("local", "n", "integer", visibility="private")
# en = Entry("local", "n", "integer", (2,1), visibility="private")
# en2 = Entry("local", "n", "integer", (), visibility="private")
# print(en1)
# print(en)
# print(en2)

#TODO
# 1) RE_READ the requirements to have them in the back of your mind
# 1) inherList
# 2) functionList?
# !) replace local by parm at class level
print("#TODO 1) inherList 2) functionList? !) replace local by parm at class level")

# class ClassEntry():
#     def __init__(self, id, inherList, dataMembeEntries, functionMembers):
#         self.category = "class"
#         self.id = id
#
#         self.inherList = ()
#         for child in inherList:
#             self.inherList += (child.data,)
#
#         # placing var data members in data table
#         self.dataMembeEntries = PrettyTable(title="data", header=False)
#         for member in dataMembeEntries:
#             if member.symRecord[0] != "function":  # var member
#                 self.dataMembeEntries.add_row(member.symRecord)
#
#         self.functionMembers = list()
#         for member in dataMembeEntries:
#             if member.symRecord[0] == "function":
#                 funcTable = PrettyTable(title="table: " + str(classtId) + "::" + str(member.symRecord[1]), header=False)
#                 funcTable.add_row(member.symRecord)
#                 classTable.add_row([funcTable])
#
#         table = PrettyTable(title="Class: " + str(self.id), header=False)
#         table.add_row("inherit", inherList, "", "")
#
#         for data in dataMembeEntries:
#             table.add_row(data)

        #
        #
        # self.functionTableList = list()
        # for func in funcEntries:
        #     self.functionTableList.append(PrettyTable(title="Function: " + str(self.id) + str(func[1]), header=False))