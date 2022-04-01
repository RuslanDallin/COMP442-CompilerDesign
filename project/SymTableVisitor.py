from Visitor import *

class SymTableVisitor (Visitor):
    def visit(self, node):

        if type(node) is progSubtree:
            implChildren = node.children[1].children
            progChildren = node.children[2].children


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
            overLoadFlag = None
            for prog in progChildren:
                name, parms = self.getFuncNameAndParam(prog.symRecord)
                for freeF in freeFuncs:
                    if freeF[0] == name:
                        overLoadFlag = True
                        if freeF[1] == parms:
                            overLoadFlag = False
                    if overLoadFlag == True:
                        error = "Overloaded free function " + str(prog.symRecord.rows[0][5])
                        ErrorList.append(error)
                    elif overLoadFlag == False:
                        error = "multiple defined free function " + str(prog.symRecord.rows[0][5])
                        ErrorList.append(error)
                freeFuncs.append(self.getFuncNameAndParam(prog.symRecord))
                node.symTable.add_row([prog.symRecord])


            self.checkUnbindedFunctions(node)
            self.checkCircular(node)



        if type(node) is implDefSubtree:

            impleFunctions = list()
            implId = node.children[0].data
            functions = node.children[1].children

            for func in functions:
                impleFunctions.append((func.symRecord))

            node.symRecord = list()
            node.symRecord.append(implId)
            node.symRecord.append(impleFunctions)

        if type(node) is structDecSubtree:
            classtId = node.children[0].data
            location = node.children[0].token.location
            inherChildren = node.children[1].children
            memberDecChildren = node.children[2].children

            classTable = PrettyTable(title="class: " + classtId, header=False)

            inherList = ()
            for child in inherChildren:
                inherList += (child.data,)

            classTable.add_row([inherList])


            #placing var data members in data table
            dataTable = PrettyTable(title="data", header=False)
            for member in memberDecChildren:
                if member.symRecord[0] != "function": #data member
                    for row in dataTable.rows:
                        if row[1] == member.symRecord[1]:
                            error = "multiple declared identifier in class " + str(member.symRecord[4])
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
                    ErrorList.append(error)
            node.symTable.add_row([node.symRecord])


        if type(node) is funcDefSubtree:
            funcId = node.children[0].data
            location = node.children[0].token.location
            funcParmsChildren = node.children[1].children
            funcType = node.children[2].data
            funcBodyChildren = node.children[3].children

            #updating local to param
            funcParams = ()
            for param in funcParmsChildren:
                print(param.symRecord)
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



                            ErrorList.append(error)
                    funcVarTable.add_row(child.symRecord.list)

            func = FunctionEntry(funcId, funcType, funcParams, visibility=None, table=funcVarTable, location=location)
            funcTable = PrettyTable(title="function: " + funcId, header=False)
            funcTable.add_row(func.list)

            node.symRecord = funcTable
            print("FuncDef")
            print(funcTable)

        if type(node) is memberDeclSubtree:
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
                    funcTable.add_row(param.symRecord.list)

            node.symRecord = FunctionEntry(funcId, funcType, funcParams, visibility=None, table=funcTable, location=location)

            print("FuncDec")
            print(funcTable)

        if type(node) is varDeclSubtree:
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

