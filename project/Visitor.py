from Nodes import *
from prettytable import PrettyTable

ErrorList = list()
ImplFunctions = list()

class Visitor:
    def __init__(self):
        self.globalTable = PrettyTable(title="table: global", header=False, hrules=True)


    def createGlobalTable(self):
        return PrettyTable(title="table: global", header=False, hrules=True)

    def getClassNames(self, node):
        sections = node.symTable.rows
        ClassNames = list()
        for table in sections:
            if table[0].title.split(" ")[0].lower() == "class:":
                ClassNames.append(table[0].title.split(" ")[1].lower())
        return ClassNames

    def getFreeNames(self, node):
        sections = node.symTable.rows
        funcNames = list()
        for table in sections:
            if table[0].title.split(" ")[0].lower() == "function:":
                funcNames.append(table[0].title.split(" ")[1].lower())
        return funcNames

    def getSubTable(self, node, className):
        sections = node.symTable.rows
        nbClasses = len(sections)
        for table in sections:
            if table[0].title.split(" ")[1].lower() == className.lower():
                return table[0]
        else:
            return str(-1)


    def getData(self, node, className):
        classTable = self.getSubTable(node, className)
        if classTable != "-1":
            dataList = list()
            for data in classTable.rows[1][0].rows:
                dataList.append(data)

            return dataList
        else:
            return str(-1)

    def addData(self, node, className, newRow):
        classTable = self.getSubTable(node, className)
        if classTable != "-1":
            classTable.rows[1][0].add_row(newRow)
        else:
            return str(-1)

    def addFunction(self, node, className, newFunc):
        classTable = self.getSubTable(node, className)
        if classTable != "-1":
            functionsTable = classTable.rows[2][0]
            functionsTable.add_row(newFunc)
        else:
            return str(-1)

    def getFunctionsTable(self, node, className):
        classTable = self.getSubTable(node, className)
        if classTable != "-1":
            functionsTable = classTable.rows[2][0]
            return functionsTable
        else:
            return str(-1)


    def getInher(self, node, className):
            classTable = self.getSubTable(node, className)
            if classTable != "-1":
                inherList = list()
                for child in classTable.rows[0][0]:
                    inherList.append(child.lower())
                return inherList
            else:
                return str(-1)

    def checkCircular(self, node):
        classList = self.getClassNames(node)
        for childClass in classList:  # for every class
            childInherList = self.getInher(node, childClass)
            for parentClass in childInherList:
                parentInherList = self.getInher(node, parentClass)
                if childClass in parentInherList:
                    error = "Circular dependence " + str(self.getSubTable(node,childClass).rows[3][0])
                    print(error)
                    ErrorList.append(error)

    def inherMigration(self, node):
        classList = self.getClassNames(node)
        for childClass in classList: # for every class 
            for parentClass in self.getInher(node, childClass): #parentClass
                if parentClass.lower() in classList:
                    parentClassData = self.getData(node, parentClass)
                    childClassData = self.getData(node, childClass)
                    parentFuncs = self.getFunctionsTable(node, parentClass)
                    childFuncs = self.getFunctionsTable(node, childClass)
                    parentVars = [row[1] for row in parentClassData]
                    childVars = [row[1] for row in childClassData]

                    #checking Shadowed
                    count = 0
                    for cVar in childVars:
                        if cVar in parentVars:
                            error = "Shadowed inherited members", childClassData[count][4]
                            print(error)
                            ErrorList.append(error)
                        count += 1

                    # adding missing
                    count = 0
                    for pVar in parentVars:
                        if pVar not in childVars:
                            self.addData(node, childClass, parentClassData[count])
                        count += 1

                    # checking for overwritten funcs
                    for cFunc in childFuncs:
                        if self.getFuncNameAndParam(cFunc) in self.getAllFuncNamesAndParms(node, parentClass):
                            error = "Overridden inherited member function " + str(cFunc.rows[0][5])
                            print(error)
                            ErrorList.append(error)

                    # adding inh funcs
                    for pFunc in parentFuncs:
                        if self.getFuncNameAndParam(pFunc) not in self.getAllFuncNamesAndParms(node, childClass):
                            self.addFunction(node,childClass, pFunc[0].rows[0])



    def getFunctionTable(self, node, functionName, params=None, className=None):
        if className:
            table = self.getSubTable(node, className)
            functionsTable = table.rows[2][0]
            for function in functionsTable:
                if function[0].rows[0][1].lower() == functionName.lower():
                    if params:
                        if function[0].rows[0][2].lower() == params:
                            return function[0]
                        else:
                            continue
                    return function[0]
            else:
                return str(-1)
        else: #free function
            return self.getSubTable(node, functionName)

    def getSetVarTable(self, node, functionName, className, newRow=None):
        funcTable = self.getFunctionTable(node, functionName, className=className)
        if funcTable != "-1":
            varTable = funcTable.rows[0][4]
            if newRow:
                varTable.add_row(newRow)
            return funcTable.rows[0][4]
        else:
            return str(-1)

    def getFuncNameAndParam(self, funcTable=None):
        if funcTable:
            return funcTable[0].rows[0][1], funcTable[0].rows[0][2]

    def getAllFuncNamesAndParms(self, node, className=None):
        nameAndParms = list()
        if className:
            table = self.getSubTable(node, className)
            functionsTable = table.rows[2][0]
            for funcTable in functionsTable:
                nameAndParms.append(self.getFuncNameAndParam(funcTable))
        else:
            freeFuncList = self.getFreeNames(node)
            for func in freeFuncList:
                funcTable = self.getSubTable(node, func)
                nameAndParms.append(self.getFuncNameAndParam(funcTable))
        return nameAndParms


    def bindFunction(self, node, funcDef, className):
        funcName = funcDef.title.split(" ")[1]

        funcDecl = self.getFunctionTable(node, functionName=funcName, className=className.lower()) #from structs
        if funcDecl == "-1":
            error = "undeclared member function definition " + str(funcDef[0].rows[0][5])
            print(error)
            ErrorList.append(error)
        else:
            if self.getFuncNameAndParam(funcDef)[0] == self.getFuncNameAndParam(funcDecl)[0]: #same name - Can be overloaded
                if self.getFuncNameAndParam(funcDef)[1] == self.getFuncNameAndParam(funcDecl)[1]: #same params - Not overloaded
                    for row in funcDef.rows[0][4].rows:
                        self.getSetVarTable(node, funcName, className, row)



    def checkUnbindedFunctions(self, node):
        for className in self.getClassNames(node):
            for pair in self.getAllFuncNamesAndParms(node, className):
                for impl in ImplFunctions:
                    if className == impl.className.lower():
                        if pair not in impl.functions:
                            if pair[0] in impl.functions[0]:
                                funcTable = self.getFunctionTable(node, pair[0], params=pair[1], className=className)
                                error = "Overloaded member function " + str(funcTable.rows[0][5])
                                print(error)
                                ErrorList.append(error)
                            else:
                                funcTable = self.getFunctionTable(node, pair[0], params=pair[1], className=className)
                                error = "undefined member function declaration " + str(funcTable.rows[0][5])
                                print(error)
                                ErrorList.append(error)


    def visit(self, node):

        if type(node) is progSubtree:
            print("visiting progSubtree")
            structChildren = node.children[0].children
            implChildren = node.children[1].children
            progChildren = node.children[2].children

            print("\n")


            print("\n")


            self.inherMigration(node)
            for impl in implChildren:
                className = impl.symRecord[0]
                group = list()
                for func in impl.symRecord[1]:
                    name, parm = self.getFuncNameAndParam(func)
                    group.append((name,parm))
                    self.bindFunction(node, func, className)
                implClass = implEntry(className,group)
                ImplFunctions.append(implClass)


            freeFuncs = list()
            overLoadFlag = False
            for prog in progChildren:
                name, parms = self.getFuncNameAndParam(prog.symRecord)
                for freeF in freeFuncs:
                    if freeF[0] == name:
                        overLoadFlag = True
                        if freeF[1] == parms:
                            overLoadFlag = False
                    if overLoadFlag:
                        error = "Overloaded free function " + str(prog.symRecord.rows[0][5])
                        print(error)
                        ErrorList.append(error)
                    else:
                        error = "multiple defined free function " + str(prog.symRecord.rows[0][5])
                        print(error)
                        ErrorList.append(error)
                freeFuncs.append(self.getFuncNameAndParam(prog.symRecord))
                node.symTable.add_row([prog.symRecord])


            self.checkUnbindedFunctions(node)
            self.checkCircular(node)

            print(node.symTable)

            print("\n")

            # 1st index is row (0-n)
            # second index is the col
            # this fetches i in the printArray table
            # print(node.symTable.rows[1][4].rows[1][1])


        if type(node) is implDefSubtree:
            print("visiting implDefSubtree")

            impleFunctions = list()
            implId = node.children[0].data
            functions = node.children[1].children

            for func in functions:
                impleFunctions.append((func.symRecord))

            node.symRecord = list()
            node.symRecord.append(implId)
            node.symRecord.append(impleFunctions)

        if type(node) is structDecSubtree:
            print("visiting structDecSubtree")
            classtId = node.children[0].data
            location = node.children[0].token.location
            inherChildren = node.children[1].children
            memberDecChildren = node.children[2].children

            classTable = PrettyTable(title="class: " + classtId, header=False)

            inherList = ()
            for child in inherChildren:
                inherList += (child.data,)

            classTable.add_row([inherList])

            # printprint(classTable)

            #placing var data members in data table
            dataTable = PrettyTable(title="data", header=False)
            for member in memberDecChildren:
                if member.symRecord[0] != "function": #data member
                    for row in dataTable.rows:
                        if row[1] == member.symRecord[1]:
                            error = "multiple declared identifier in class " + str(member.symRecord[4])
                            print(error)
                            ErrorList.append(error)
                    dataTable.add_row(member.symRecord)



            classTable.add_row([dataTable])

            functionsTable = PrettyTable(title="functions ", header=False, hrules=True)
            for member in memberDecChildren:
                if member.symRecord[0] == "function":
                    functionsTable.add_row(member.symRecord)


            classTable.add_row([functionsTable])
            classTable.add_row([location])
            node.symRecord = classTable

            for row in  node.symTable.rows:
                if row[0].title == node.symRecord.title:
                    error = "multiply declared class " + str(node.symRecord.rows[3][0])
                    print(error)
                    ErrorList.append(error)
            node.symTable.add_row([node.symRecord])


        if type(node) is funcDefSubtree:
            print("visiting funcBodySubtree")
            funcId = node.children[0].data
            location = node.children[0].token.location
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
            funcVarTable = PrettyTable(title="table: " + funcId, header=False)
            for child in funcBodyChildren:
                if child.__class__.__name__ == "varDeclSubtree":
                    for row in funcVarTable.rows:
                        if row[1] == child.symRecord.id:
                            error = "multiple declared identifier in function " + str(child.symRecord.list[4])
                            print(error)
                            ErrorList.append(error)
                    funcVarTable.add_row([x for x in child.symRecord.list if x])

            func = FunctionEntry(funcId, funcType, funcParams, visibility=None, table=funcVarTable, location=location)
            funcTable = PrettyTable(title="function: " + funcId, header=False)
            funcTable.add_row(func.list)

            node.symRecord = funcTable

        if type(node) is memberDeclSubtree:
            print("visiting memberDeclSubtree")
            visibility = node.children[0].data
            if node.children[1].__class__.__name__ == "varDeclSubtree":
                varRecord = node.children[1].symRecord.list
                varRecord[3] = visibility
                varRecord[0] = "data"
                node.symRecord = varRecord
            if node.children[1].__class__.__name__ == "funcDeclSubtree":
                funcRecord = node.children[1].symRecord.list
                funcRecord[3] = visibility
                node.symRecord = funcRecord


        if type(node) is funcDeclSubtree:
            print("visiting funcDeclSubtree")
            funcId = node.children[0].data
            location = node.children[0].token.location
            funcParmsChildren = node.children[1].children
            funcType = node.children[2].data


            #updating local to param
            funcParams = ()
            funcTable = PrettyTable(title="table: " + funcId, header=False)
            for param in funcParmsChildren:
                if param.__class__.__name__ == "varDeclSubtree":
                    param.symRecord.list[0] = "param"
                    funcParams += (param.symRecord.list[2],)
                    funcTable.add_row([x for x in param.symRecord.list if x])

            node.symRecord = FunctionEntry(funcId, funcType, funcParams, visibility=None, table=funcTable, location=location)


        if type(node) is varDeclSubtree:
            print("visiting varDeclSubtree")
            varName = node.children[0].data
            location = node.children[0].token.location
            varType = node.children[1].data
            dimListChildren = node.children[2].children
            varDimlist = list()
            for arrSize in dimListChildren:
                if len(arrSize.children) > 0: #[3]
                    varDimlist.append("[" + str(arrSize.children[0].data) + "]")
                else: #[]
                    varDimlist.append("[]")
            entry = Entry(varName, varType, varDimlist, location=location)
            node.symRecord = entry

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
    def __init__(self, id, type, dimList="", visibility="", location=""):
        self.category = "local"
        self.id = id
        self.type = type
        self.dimList = dimList
        self.visibility = visibility
        self.dimStr = ""
        self.location = location
        if self.dimList != "":
            for dim in self.dimList:
                self.dimStr += dim
        self.list = [self.category, self.id, str(self.type) + str(self.dimStr),  self.visibility, self.location]

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
    def __init__(self, id, type, parms, visibility="", table="", location=""):
        self.category = "function"
        self.id = id
        self.location =location

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

        self.list = [self.category, self.id, self.parms, self.visibility, self.table, self.location]


class implEntry():
    def __init__(self, className, functions):
        self.className = className
        self.functions = functions

    def __str__(self):
        return "%s => %s" % (self.className, self.functions)

#not used
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

