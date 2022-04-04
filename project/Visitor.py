from Nodes import *
from prettytable import PrettyTable

ErrorList = list()
ImplFunctions = list()

class Visitor:
    def __init__(self):
        self.globalTable = PrettyTable(title="table: global", header=False, hrules=True)

    def visit(self, node): pass

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
            counter = 0
            for row in varTable.rows:
                if row[1] == newRow[1]:
                    varTable.del_row(counter)
                    varTable.add_row(newRow)
                    break
                    counter += 1
            else:
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
                                ErrorList.append(error)
                            else:
                                funcTable = self.getFunctionTable(node, pair[0], params=pair[1], className=className)
                                error = "undefined member function declaration " + str(funcTable.rows[0][5])
                                ErrorList.append(error)


# ============================================================================================================


    def callAccept(self, node):
        for child in node.children:
            child.symTable = node.symTable
            if node.counter:
                child.counter = node.counter
            child.accept(self)
        self.visit(self)

    def addTempVar(self, node, type="integer", location="", offset=4):
        varName = "t" + str(node.counter[-1])
        if type == "integer": offset = 4
        if type == "float": offset = 8
        name = "temp" + node.name.title()
        return [name, varName, type, "", location, offset]


    def anchestorFunc(self, node):
        for a in node.anchestors:
            if a.name == "funcDef":
                return a.symRecord

    def anchestorVars(self, node):
        func = self.anchestorFunc(node)
        return func.rows[0][4]

    def anchestorClassName(self, node):
        for parent in node.anchestors:
            if parent.name == "implDef":
                return parent.children[0].data



    def addVar(self, node, varEntry):
        varTable = self.anchestorVars(node)
        varTable.add_row(varEntry)

    def fetchLocation(self, node):
        for child in node.descendants:
            if child.token != None:
                return child.token.location

    def getFuncReturnType(self, node, funcId, classPar=None):
        func = self.getMultiTable(node, funcId, classPar)
        paramsLine = func.rows[0][2]
        return paramsLine.split(":")[1]

    def getClassScope(self, node, classPar):
        return self.getMultiTable(node, classPar=classPar).rows[-1][0]

    def getMultiTable(self, node, funcPar=None, classPar=None):
        # if className emoty means it's a free func
        if classPar:
            for row in node.symTable.rows:
                if row[0].title.startswith("class:"):
                    className = row[0].title.split(" ")[1]
                    if className.lower() == classPar.lower():

                        if funcPar == None: # if funcPar is empty, this method returns a class
                            return row[0]

                        funcsTable = row[0][2][0] # else, return the class's funcPar
                        for funcs in funcsTable.rows:
                            for func in funcs[0]:
                                funcName = func.rows[0][1]
                                if funcName.lower() == funcPar.lower():
                                    return func

        else:  # if classPar is empty, this method returns the funcPar free function
            for row in node.symTable.rows:
                if row[0].title.startswith("function:"):
                    funcName = row[0].rows[0][1]
                    if funcName.lower() == funcPar.lower():
                        return row[0]

    def getMain(self, node):
        return self.getFunctionTable(node, functionName="main", params="():void")

    # not used but could be useful
    def getAllVarTables(self, node):
        for row in node.symTable.rows:
            if row[0].title.startswith("class:"):
                className = row[0].title.split(" ")[1]
                funcsTable = row[0][2][0]

                for funcs in funcsTable.rows:
                    for func in funcs[0]:
                        self.addCumulativeOffset(node, func)
            else:  # free funcs
                self.addCumulativeOffset(node, row[0])

    def addCumulativeOffset(self, node, funcTable):
        mainFunc = self.getMain(node)

        if funcTable.get_string() == mainFunc.get_string():
            offSetCounter = 0 #main func so lowest offset
        else:
            offSetCounter = -8 # reserve two spaces on stack for jump and return

        offSetTotalCol = list()

        varTable = funcTable.rows[0][4]
        for entry in varTable.rows:

            try:
                offSetCounter -= int(entry[-1])
            except:  # if type is a class type
                entry[-1] = -self.getClassScope(node, classPar=entry[-1])
                if entry[-1] == None:
                    error = "Undeclared class" + str(entry[-2])
                    ErrorList.append(error)
                offSetCounter -= int(entry[-1])

            offSetTotalCol.append(offSetCounter)
        varTable.add_column(fieldname="cumul", column=offSetTotalCol)


# ============================================================================================================



class Entry():
    def __init__(self, id, type, dimList="", visibility="", location="", dimOffSet=1):
        self.category = "local"
        self.id = id
        self.type = type
        self.dimList = dimList
        self.visibility = visibility
        self.dimStr = ""
        self.location = location
        self.offset = ""

        if type == "integer": self.offset = 4 * dimOffSet
        elif type == "float": self.offset = 8 * dimOffSet
        else:
            self.offset = type

        if self.dimList != "":
            for dim in self.dimList:
                self.dimStr += dim

        self.list = [self.category, self.id, str(self.type) + str(self.dimStr),  self.visibility, self.location, self.offset]

    def __str__(self):
        if self.dimList and self.visibility:
            return "%s\t | %s\t | %s%s\t | %s" % (self.category, self.id, self.type, self.dimStr, self.visibility)
        if self.dimList:
            return "%s\t | %s\t | %s%s\t" % (self.category, self.id, self.type, self.dimStr)
        if self.visibility:
            return "%s\t | %s\t | %s\t | %s\t" % (self.category, self.id, self.type, self.visibility)
        else:
            return "%s\t | %s\t | %s\t" % (self.category, self.id, self.type)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.id == other.id and self.dimStr == other.dimStr
        else:
            return False

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