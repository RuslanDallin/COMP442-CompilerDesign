from Visitor import *


class CodeGenerationVisitor(Visitor):
    def __init__(self):
        self.registerStack = list()
        self.moonCode = list()
        for r in range (12, 0, -1):
            self.registerStack.append("r" + str(r))

    def visit(self, node):

        if type(node) is progSubtree:
            print(node.symTable)
            entry = "entry \naddi r14, r0, topaddr"
            print(self.moonAppendText(entry))

            print("\n")
            self.callAccept(node)

            halt = "hlt \nbuf res 20"
            print(self.moonAppendText(halt))

        if type(node) is funcDefSubtree:
            node.counter.pop()
            for i in range (len(node.counter)):
                node.counter[i] = "t" + str(node.counter[i])
            node.counter.reverse()
            self.callAccept(node)

        if type(node) is assignSubtree:
            self.callAccept(node)
            tempReg = self.registerStack.pop()

            leftData = node.children[0].data
            if leftData:
                leftOff = self.getOffset(node, leftData)
            else:
                leftOff = self.getOffset(node, node.counter.pop())
            # print("Left", leftData, leftOff, tempReg)

            right = node.children[1].data
            rightData = self.getValue(right)
            # print("right", right, rightData)

            if rightData: # x = 2
                comment = "% assigning " + str(leftData) + " = " + str(rightData)
                print(self.moonAppendText(comment))

                rightAdd = self.moonAddi(tempReg, "r0", rightData)
                print(rightAdd)
            else: # x = t1
                comment = "% initializing " + str(leftData) + " = " + str(right)
                print(self.moonAppendText(comment))

                rightOff = self.getOffset(node, right)
                rightLoad = self.moonLW(tempReg, rightOff)
                print(rightLoad)

            moonSW = self.moonSW(leftOff, tempReg)
            print(moonSW)

            self.registerStack.append(tempReg)

            print("\n")

            # print("leftA", node.children[0].data)
            # print("rightA", node.children[1].data)

        if "OpSubtree" in node.__class__.__name__:
            self.callAccept(node)

            tempReg = self.registerStack.pop()
            tempVar = node.counter.pop()
            tempOff = self.getOffset(node, tempVar)
            node.data = tempVar # set the temp var as data
            sign = node.children[1].data
            operation = self.signConvert(sign)
            # print("\n", operation, tempReg, tempOff)

            leftReg = self.registerStack.pop()
            leftData = node.children[0].data
            if leftData:
                leftOff = self.getOffset(node, leftData)
            else: # not a var or a int prob func call
                leftOff = self.getOffset(node, node.counter.pop())
            # print("Left", leftData, leftOff, leftReg)

            rightReg = self.registerStack.pop()
            rightData = node.children[2].data
            if rightData:
                rightOff = self.getOffset(node, rightData)
            else: # not a var or a int prob func call
                rightOff = self.getOffset(node, node.counter.pop())
            # print("right", rightData, rightOff, rightReg)

            # print("\n")

            leftValue = self.getValue(leftData)
            rightValue = self.getValue(rightData)

            if leftValue:
                left = self.moonAddi(leftReg, "r0", leftValue)
            else:
                left = self.moonLW(leftReg, leftOff)

            if rightValue:
                right = self.moonAddi(rightReg, "r0", rightValue)
            else:
                right =  self.moonLW(rightReg, rightOff)

            calculate = self.moonCalculate(operation, tempReg, leftReg, rightReg)
            store = self.moonSW(tempOff, tempReg)

            comment = "% " + tempVar + " = " + leftData + " " + sign + " " +rightData
            self.moonAppendText(comment)
            print(comment)

            print(left)
            print(right)
            print(calculate)
            print(store)

            self.registerStack.append(tempReg)
            self.registerStack.append(leftReg)
            self.registerStack.append(rightReg)

            print("\n")

        if type(node) is writeSubtree:
            self.callAccept(node)
            expr = node.children[0].data
            expOffset = self.getOffset(node,expr)
            tempReg = self.registerStack.pop()
            load = self.moonLW(tempReg, expOffset)
            self.moonCode.append(load)

            print(load)

            comment = "% incrementing stack frame and starting printing"
            print(comment)
            self.moonAppendText(comment)

            pushStackFrame = self.moonAddi("r14", "r14", self.anchestorFuncScope(node))
            print(pushStackFrame)


            printLib = "sw -8(r14),r1 \n" \
                    "addi r1,r0, buf \n" \
                    "sw -12(r14),r1 \n" \
                    "jl r15, intstr \n" \
                    "sw -8(r14),r13 \n" \
                    "jl r15, putstr \n" \
                    "subi r14,r14,-24 \n"

            self.moonCode.append(printLib)

            print(printLib)



        if type(node) is factorSubtree: self.callAccept(node)

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
        return varTable.rows[-1][-1] + -4

    def moonLW(self, reg, offset):
        code = "lw" + " " + reg + ", " + offset + "(r14)"
        self.moonCode.append(code)
        return code

    def moonCalculate(self, operation, tempReg, leftReg, rightReg):
        code = operation + " " + tempReg + ", " + leftReg + ", " + rightReg
        self.moonCode.append(code)
        return code


    def moonSW(self, tempOff, tempReg):
        code = "sw " + tempOff + "(r14), " + tempReg
        self.moonCode.append(code)
        return code

    def moonAddi(self, reg1, reg2, value):
        code = "addi " + reg1 + ", " + reg2 + ", " + str(value)
        self.moonCode.append(code)
        return code

    def moonAppendText(self, string):
        code = string
        self.moonCode.append(code)
        return code

    def getValue(self, data):
        try:
            return int(data)
        except:
            try:
                return float(data)
            except:
                return None





