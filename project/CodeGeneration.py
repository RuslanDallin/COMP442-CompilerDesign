from Visitor import *

moonCode = list()

class CodeGenerationVisitor(Visitor):
    def __init__(self):
        self.registerStack = list()
        self.ifElseCounter = 0
        for r in range (12, 0, -1):
            self.registerStack.append("r" + str(r))

    def visit(self, node):

        if type(node) is progSubtree:
            self.callAccept(node)

            halt = "hlt \nbuf res 20"
            self.moonAppendText(halt)

        if type(node) is funcDefSubtree:
            node.counter.pop()
            for i in range (len(node.counter)): #use this counter to know which t1..tn to use
                node.counter[i] = "t" + str(node.counter[i])
            node.counter.reverse()
            halt = "hlt \nbuf res 20"

            main = self.getMain(node)
            if node.symRecord.get_string() == main.get_string():
                entry = "% start of main\n" \
                    + "entry \naddi r14, r0, topaddr \n"
            else:
                entry = "% start of " + str(node.symRecord.rows[0][1]) + "\n" \
                        + str(node.symRecord.rows[0][1]) + " sw -8(r14), r15"

            self.moonAppendText(entry)
            self.moonAppendText("\n")

            self.callAccept(node)

        if type(node) is assignSubtree:
            self.callAccept(node)
            tempReg = self.registerStack.pop()

            leftData = node.children[0].data
            leftOff = self.getOffset(node, leftData)
            # print("Left", leftData, leftOff, tempReg)

            rightData = node.children[1].data
            rightValue = self.getValue(rightData)
            # print("right", right, rightData)

            if rightValue != None: # x = 2
                comment = "		% assigning " + str(leftData) + " = " + str(rightData)
                addi = self.moonAddi(tempReg, "r0", rightValue, comment)
            else: # x = t1
                comment = "		% assigning " + str(leftData) + " = " + str(rightData)
                load =  self.moonLW(tempReg, self.getOffset(node, rightData), comment)

            moonSW = self.moonSW(leftOff, tempReg)
            self.registerStack.append(tempReg)
            self.moonAppendText("\n")


        if "OpSubtree" in node.__class__.__name__:
            self.callAccept(node)

            leftReg = self.registerStack.pop()
            leftData = node.children[0].data
            leftOff = self.getOffset(node, leftData)
            leftValue = self.getValue(leftData)
            # print("Left", leftData, leftOff, leftReg, leftValue)

            rightReg = self.registerStack.pop()
            rightData = node.children[2].data
            rightOff = self.getOffset(node, rightData)
            rightValue = self.getValue(rightData)
            # print("right", rightData, rightOff, rightReg, rightValue)


            tempReg = self.registerStack.pop()
            tempVar = node.counter.pop()
            tempOff = self.getOffset(node, tempVar)
            node.data = tempVar # set the temp var as data
            sign = node.children[1].data
            operation = self.signConvert(sign)
            # print("\n", operation, tempReg, tempOff)

            comment = "		% " + str(tempVar) + " = " + str(leftData) + " " + sign + " " + str(rightData)
            if leftValue != None: # 67 + x
                left = self.moonAddi(leftReg, "r0", leftValue, comment)
            else: # x + x
                left = self.moonLW(leftReg, leftOff, comment)

            if rightValue != None: # x + 67
                right = self.moonAddi(rightReg, "r0", rightValue)
            else: # x + x
                right =  self.moonLW(rightReg, rightOff)

            calculate = self.moonCalculate(operation, tempReg, leftReg, rightReg)
            store = self.moonSW(tempOff, tempReg)

            self.registerStack.append(tempReg)
            self.registerStack.append(rightReg)
            self.registerStack.append(leftReg)
            self.moonAppendText("\n")

        if type(node) is writeSubtree:
            self.callAccept(node)

            tempReg = self.registerStack.pop()
            expr = node.children[0].data
            exprValue = self.getValue(expr)
            expOffset = self.getOffset(node, expr)
            if exprValue != None: # write (7)
                comment = "		% loading " + str(exprValue)
                addi = self.moonAddi(tempReg, "r0", exprValue, comment)
            else: # write (x)
                comment = "		% loading " + expr
                load = self.moonLW(tempReg, expOffset, comment)


            comment = "		% incrementing stack frame and starting printing"
            pushStackFrame = self.moonAddi("r14", "r14", self.anchestorFuncScope(node), comment)

            printLib = "sw -8(r14),r1 \n" \
                       "addi r1,r0, buf \n" \
                       "sw -12(r14),r1 \n" \
                       "jl r15, intstr \n" \
                       "sw -8(r14),r13 \n" \
                       "jl r15, putstr "
            moonCode.append(printLib)

            comment = "		% decremeting stack frame and starting printing"
            pushStackFrame = self.moonSubi("r14", "r14", self.anchestorFuncScope(node), comment)
            self.registerStack.append(tempReg)
            self.moonAppendText("\n")


        if type(node) is funCallSubtree:
            self.callAccept(node)

            tempReg = self.registerStack.pop()
            functionName = node.children[0].data

            params = self.getParams(node, functionName)
            if params == None:
                return
            for child in node.children[1].children:
                param = params.pop()
                parmNewoffset = param[-1] + self.anchestorFuncScope(node)

                comment = "		% pass " + str(child.data) + " into " + str(param[1])
                load = self.moonLW(tempReg, self.getOffset(node, child.data), comment)
                store = self.moonSW(parmNewoffset, tempReg)
            self.moonAppendText("\n")

            comment = "		% increment stack frame"
            incr = self.moonAddi("r14", "r14", self.anchestorFuncScope(node), comment)

            jump = self.moonJL(functionName)

            comment = "		% decrement stack frame"
            decr = self.moonSubi("r14", "r14", self.anchestorFuncScope(node), comment)
            tempVar = node.counter.pop()

            comment = "		% " + tempVar + " = " + functionName
            load = self.moonLW(tempReg, self.anchestorFuncScope(node), comment)
            store = self.moonSW(self.getOffset(node,tempVar), tempReg)

            node.data = tempVar
            node.parent.data = node.data
            self.registerStack.append(tempReg)
            self.moonAppendText("\n")

        if type(node) is returnSubtree:
            self.callAccept(node)

            tempReg = self.registerStack.pop()
            var = node.children[0].data
            comment = "		% return " + var
            load = self.moonLW(tempReg, self.getOffset(node,var), comment)
            store = self.moonSW("0", tempReg)


            comment = "		% jump to calling function "
            load = self.moonLW("r15", "-8", comment)
            jump = self.moonJR()

            self.registerStack.append(tempReg)
            self.moonAppendText("\n")


        if type(node) is factorSubtree:
            self.callAccept(node)

            if len(node.children) > 1:
                if node.children[1].children[0].name == "var": # negated
                    tempReg = self.registerStack.pop()
                    var = node.children[1].data
                    comment = "		% neg " + var
                    load = self.moonLW(tempReg, self.getOffset(node, var), comment)
                    muli = "muli " + tempReg + ", " + tempReg + ", -1"
                    self.moonAppendText(muli)
                    store = self.moonSW(self.getOffset(node, var), tempReg)
                    self.registerStack.append(tempReg)
                    self.moonAppendText("\n")
                else: # a number
                    node.data = "-" + node.children[1].data

        if type(node) is ifThenElseSubtree:
            # self.callAccept(node)

            tempReg = self.registerStack.pop()
            self.ifElseCounter += 1
            exprVar = node.children[0]
            for child in exprVar.children:
                child.accept(self)
            expr = exprVar.children[0].data

            exprValue = self.getValue(expr)
            expOffset = self.getOffset(node, expr)
            if exprValue != None: # write (7)
                comment = "		% loading " + str(exprValue)
                addi = self.moonAddi(tempReg, "r0", exprValue, comment)
            else: # write (x)
                comment = "		% loading " + expr
                load = self.moonLW(tempReg, expOffset, comment)


            elseFlag = "else" + str(self.ifElseCounter)
            endIfFlag = "endIf" + str(self.ifElseCounter)
            expr = self.moonBZ(tempReg, elseFlag) # Branching here
            self.registerStack.append(tempReg)
            self.moonAppendText("\n")

            tempReg = self.registerStack.pop()
            ifTree = node.children[1]
            for child in ifTree.children:
                child.accept(self)
            jump = moonCode.append("j " + endIfFlag)
            self.registerStack.append(tempReg)

            tempReg = self.registerStack.pop()
            elseTree = node.children[2]
            elseLabel = moonCode.append(elseFlag + " nop")
            for child in elseTree.children:
                child.accept(self)
            endIf = moonCode.append(endIfFlag + " nop")
            self.registerStack.append(tempReg)

        if type(node) is implDefSubtree: self.callAccept(node)

        if type(node) is structDecSubtree: self.callAccept(node)

        if type(node) is memberDeclSubtree: self.callAccept(node)

        if type(node) is funcDeclSubtree: self.callAccept(node)

        if type(node) is varDeclSubtree: self.callAccept(node)

        if type(node) is Node: self.callAccept(node)

        if type(node) is IdNode: self.callAccept(node)

        if type(node) is MulOpNode: self.callAccept(node)

        if type(node) is aParamsSubtree: self.callAccept(node)

        if type(node) is addOpNode: self.callAccept(node)

        # if type(node) is addOpSubtree: self.callAccept(node)


        if type(node) is dimListSubtree: self.callAccept(node)

        if type(node) is dotSubtree: self.callAccept(node)

        if type(node) is floatNode: self.callAccept(node)

        if type(node) is fparmListSubtree: self.callAccept(node)

        if type(node) is funcBodySubtree: self.callAccept(node)

        if type(node) is funcDefListSubtree: self.callAccept(node)

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

        if type(node) is signNode: self.callAccept(node)

        if type(node) is statSubtree: self.callAccept(node)

        if type(node) is structDecListSubtree: self.callAccept(node)

        if type(node) is typeNode: self.callAccept(node)

        if type(node) is varSubtree: self.callAccept(node)

        if type(node) is visibilityNode: self.callAccept(node)

        if type(node) is whileSubtree: self.callAccept(node)




    def callAccept(self, node):
        for child in node.children:
            child.accept(self)
        self.visit(self)

    def signConvert(self, charSign):
        sign = ""
        if charSign == '+' : sign = "add"
        if charSign == '-' : sign = "sub"
        if charSign == '*' : sign = "mul"
        if charSign == '/' : sign = "div"
        if charSign == '&' : sign = "and"
        if charSign == '|' : sign = "or"
        if charSign == '!' : sign = "not"
        if charSign == '==' : sign = "ceq"
        if charSign == '<>' : sign = "cne"
        if charSign == '<' : sign = "clt"
        if charSign == '<=' : sign = "cle"
        if charSign == '>' : sign = "cgt"
        if charSign == '>=' : sign = "cge"
        return sign

    def getOffset(self, node, varName):
        varTable = self.anchestorVars(node)
        for entry in varTable.rows:
            if entry[1] == varName:
                return str(entry[-1])
        else:
            return "None"


    def anchestorFuncScope(self, node):
        varTable = self.anchestorVars(node)
        return varTable.rows[-1][-1] -4

    def moonLW(self, reg, offset, comment=""):
        code = "lw" + " " + reg + ", " + str(offset) + "(r14)" + comment
        moonCode.append(code)
        return code

    def moonCalculate(self, operation, tempReg, leftReg, rightReg, comment=""):
        code = operation + " " + tempReg + ", " + leftReg + ", " + rightReg + comment
        moonCode.append(code)
        return code

    def moonSW(self, tempOff, tempReg, comment=""):
        code = "sw " + str(tempOff) + "(r14), " + tempReg + comment
        moonCode.append(code)
        return code

    def moonAddi(self, reg1, reg2, value, comment=""):
        code = "addi " + reg1 + ", " + reg2 + ", " + str(value) + comment
        moonCode.append(code)
        return code

    def moonSubi(self, reg1, reg2, value, comment=""):
        code = "subi " + reg1 + ", " + reg2 + ", " + str(value) + comment
        moonCode.append(code)
        return code

    def moonAppendText(self, string):
        code = string
        moonCode.append(code)
        return code

    def moonJL(self, funcName, comment=""):
        code = "jl r15, " + funcName + comment
        moonCode.append(code)
        return code

    def moonJR(self, comment=""):
        code = "jr r15 "+ comment
        moonCode.append(code)
        return code

    def moonBZ(self, tempReg, label, comment=""):
        code = "bz " + tempReg + " , " + label + comment
        moonCode.append(code)
        return code

    def getValue(self, data):
        if data == "0": return 0
        try:
            return int(data)
        except:
            try:
                return float(data)
            except:
                return None

    def getVars(self, node, functionName, className=None):
        if className:
            func = self.getMultiTable(node, funcPar=functionName, classPar=className)
        else: #free function
            func = self.getMultiTable(node, funcPar=functionName)
            if func == None:
                return
        return func.rows[0][4].rows

    def getParams(self, node, functionName, className=None):
        listOfParms = list()
        vars = self.getVars(node, functionName, className=className)
        if vars == None:
            return
        for var in vars:
            if var[0] == "param":
                listOfParms.append(var)
        listOfParms.reverse()
        return listOfParms







