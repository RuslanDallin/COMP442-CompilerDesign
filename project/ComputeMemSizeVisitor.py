from Visitor import *

class ComputeMemSizeVisitor(Visitor):


    def visit(self, node):

        if "OpSubtree" in node.__class__.__name__:
            self.callAccept(node)

            leftChild = node.children[0]
            rightChild = node.children[2]

            if leftChild.type != rightChild.type:
                print("=>", node.name)
                print(leftChild.type, rightChild.type)
                error = "invalid to have operands of arithmetic operators to be of different types " + str(self.fetchLocation(node))
                ErrorList.append(error)
                node.type = "integer"
            else:
                node.type = leftChild.type

            tempVar = self.addTempVar(node, node.type, self.fetchLocation(node))
            self.addVar(node, tempVar)
            node.counter.append(node.counter[-1] + 1)

        if type(node) is progSubtree:
            self.callAccept(node)
            print(self.getAllVarTables(node))




        if type(node) is factorSubtree:
            self.callAccept(node)
            child = node.children[0]
            if child.name == "float": child.type = "float"
            if child.name == "num": child.type = "integer"
            node.data = child.data
            if child.name == "var":
                node.data = child.children[0].data
                varTable = self.anchestorVars(node)
                for varEntry in varTable.rows:
                    if node.data == varEntry[1]:
                        child.type = varEntry[2]
                        break
                else:
                    classname = self.anchestorClassName(node)
                    if classname:
                        dataTable = self.getData(node, className=classname)
                        for entry in dataTable:
                            if node.data == entry[1]:
                                child.type = entry[2]

            if child.name == "funCall":
                funcId = child.children[0].data
                child.type = self.getFuncReturnType(node, funcId)
                if child.type == "int": child.type = "integer"

                tempVar = self.addTempVar(node, child.type, self.fetchLocation(node))
                self.addVar(node, tempVar)
                node.counter.append(node.counter[-1] + 1)

            node.type = child.type




        if type(node) is implDefSubtree: self.callAccept(node)

        if type(node) is structDecSubtree: self.callAccept(node)

        if type(node) is funcDefSubtree: self.callAccept(node)

        if type(node) is memberDeclSubtree: self.callAccept(node)

        if type(node) is funcDeclSubtree: self.callAccept(node)

        if type(node) is varDeclSubtree: self.callAccept(node)

        if type(node) is Node: self.callAccept(node)

        if type(node) is IdNode: self.callAccept(node)

        if type(node) is MulOpNode: self.callAccept(node)

        if type(node) is aParamsSubtree: self.callAccept(node)

        if type(node) is addOpNode: self.callAccept(node)

        # if type(node) is addOpSubtree: self.callAccept(node)

        if type(node) is assignSubtree: self.callAccept(node)

        if type(node) is dimListSubtree: self.callAccept(node)

        if type(node) is dotSubtree: self.callAccept(node)


        if type(node) is floatNode: self.callAccept(node)

        if type(node) is fparmListSubtree: self.callAccept(node)

        if type(node) is funCallSubtree: self.callAccept(node)

        if type(node) is funcBodySubtree: self.callAccept(node)

        if type(node) is funcDefListSubtree: self.callAccept(node)

        if type(node) is ifThenElseSubtree: self.callAccept(node)

        if type(node) is implDefListSubtree: self.callAccept(node)

        if type(node) is indiceListSubtree: self.callAccept(node)

        if type(node) is inherListSubtree: self.callAccept(node)

        if type(node) is memberDeclListSubtree: self.callAccept(node)

        # if type(node) is mulOpSubtree: self.callAccept(node)

        if type(node) is numNode: self.callAccept(node)

        if type(node) is readSubtree: self.callAccept(node)

        if type(node) is relExprSubtree: self.callAccept(node)

        if type(node) is relOpNode: self.callAccept(node)

        # if type(node) is relOpSubtree: self.callAccept(node)

        if type(node) is returnSubtree: self.callAccept(node)

        if type(node) is signNode: self.callAccept(node)

        if type(node) is statSubtree: self.callAccept(node)

        if type(node) is structDecListSubtree: self.callAccept(node)

        if type(node) is typeNode: self.callAccept(node)

        if type(node) is varSubtree:
            self.callAccept(node)
            node.data = node.children[0].data

        if type(node) is visibilityNode: self.callAccept(node)

        if type(node) is whileSubtree: self.callAccept(node)

        if type(node) is writeSubtree: self.callAccept(node)

    # def callAccept(self, node):
    #     for child in node.children:
    #         child.symTable = node.symTable
    #         if node.counter:
    #             child.counter = node.counter
    #         child.accept(self)
    #     self.visit(self)
    #
    # def addTempVar(self, node, type="integer", location="", offset=4):
    #     varName = "t" + str(node.counter[-1])
    #     if type == "integer": offset = 4
    #     if type == "float": offset = 8
    #     name = "temp" + node.name.title()
    #     return [name, varName, type, "", location, offset]
    #
    #
    # def anchestorFunc(self, node):
    #     for a in node.anchestors:
    #         if a.name == "funcDef":
    #             return a.symRecord
    #
    # def anchestorVars(self, node):
    #     func = self.anchestorFunc(node)
    #     return func.rows[0][4]
    #
    # def anchestorClassName(self, node):
    #     for parent in node.anchestors:
    #         if parent.name == "implDef":
    #             return parent.children[0].data
    #
    #
    #
    # def addVar(self, node, varEntry):
    #     varTable = self.anchestorVars(node)
    #     varTable.add_row(varEntry)
    #
    # def fetchLocation(self, node):
    #     for child in node.descendants:
    #         if child.token != None:
    #             return child.token.location
    #
    # def getFuncReturnType(self, node, funcId, classPar=None):
    #     func = self.getMultiTable(node, funcId, classPar)
    #     paramsLine = func.rows[0][2]
    #     return paramsLine.split(":")[1]
    #
    # def getClassScope(self, node, classPar):
    #     return self.getMultiTable(node, classPar=classPar).rows[-1][0]
    #
    # def getMultiTable(self, node, funcPar=None, classPar=None):
    #     # if className emoty means it's a free func
    #     if classPar:
    #         for row in node.symTable.rows:
    #             if row[0].title.startswith("class:"):
    #                 className = row[0].title.split(" ")[1]
    #                 if className.lower() == classPar.lower():
    #
    #                     if funcPar == None: # if funcPar is empty, this method returns a class
    #                         return row[0]
    #
    #                     funcsTable = row[0][2][0] # else, return the class's funcPar
    #                     for funcs in funcsTable.rows:
    #                         for func in funcs[0]:
    #                             funcName = func.rows[0][1]
    #                             if funcName.lower() == funcPar.lower():
    #                                 return func
    #
    #     else:  # if classPar is empty, this method returns the funcPar free function
    #         for row in node.symTable.rows:
    #             if row[0].title.startswith("function:"):
    #                 funcName = row[0].rows[0][1]
    #                 if funcName.lower() == funcPar.lower():
    #                     return row[0]
    #
    # def getMain(self, node):
    #     return self.getFunctionTable(node, functionName="main", params="():void")
    #
    # # not used but could be useful
    # def getAllVarTables(self, node):
    #     for row in node.symTable.rows:
    #         if row[0].title.startswith("class:"):
    #             className = row[0].title.split(" ")[1]
    #             funcsTable = row[0][2][0]
    #
    #             for funcs in funcsTable.rows:
    #                 for func in funcs[0]:
    #                     self.addCumulativeOffset(node, func)
    #         else:  # free funcs
    #             self.addCumulativeOffset(node, row[0])
    #
    # def addCumulativeOffset(self, node, funcTable):
    #     mainFunc = self.getMain(node)
    #
    #     if funcTable.get_string() == mainFunc.get_string():
    #         offSetCounter = 0 #main func so lowest offset
    #     else:
    #         offSetCounter = -8 # reserve two spaces on stack for jump and return
    #
    #     offSetTotalCol = list()
    #
    #     varTable = funcTable.rows[0][4]
    #     for entry in varTable.rows:
    #
    #         try:
    #             offSetCounter -= int(entry[-1])
    #         except:  # if type is a class type
    #             entry[-1] = -self.getClassScope(node, classPar=entry[-1])
    #             if entry[-1] == None:
    #                 error = "Undeclared class" + str(entry[-2])
    #                 ErrorList.append(error)
    #             offSetCounter -= int(entry[-1])
    #
    #         offSetTotalCol.append(offSetCounter)
    #     varTable.add_column(fieldname="cumul", column=offSetTotalCol)