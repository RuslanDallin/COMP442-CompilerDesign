import os
import pandas as pd
from anytree import RenderTree

from LexicalAnalyzer import *
import Nodes


ParseTable = pd.read_csv("AttributeParsingTable.csv")
ParseTable.set_index("TT", inplace=True)
FFTable = pd.read_csv("FirstFollowSets.csv")
FFTable.set_index("nonterminal", inplace=True)

prodStack = []
semanticStack = []

def isTerminal(s):
    return (s in LexemeDic.values()) or (s in reservedWords) or (s == "id")

def getTableReversedRHS(row,token,PrevDeriv):
    rhs= -1  # -1: no column match
    newDeriv = PrevDeriv
    col = token.type
    if col in ParseTable.columns:
        rhs = str(ParseTable[col][row])
        if rhs == "nan":
            rhs = 0  # 0: cell is empty
        else:
            newDeriv = derivationBuilder(derivationKeywordReplace(rhs),PrevDeriv) # updates derivation
            arrowIndex = rhs.index("→ ") + 2
            trucatedRhs = rhs[arrowIndex:]
            rhs = reverseSentence(trucatedRhs) + " "
    if rhs == -1:
        printTransitions(row) # For debugging purposes
    return str(rhs), newDeriv

def printTransitions(row):
    cols = ParseTable.columns
    for c in cols:
        value = ParseTable[c][row]
        if str(value) != "nan":
            print(row, ",", c, " => ", value)

def reverseSentence(s):
    tempList = s.split()
    reversedList = reversed(tempList)
    return " ".join(reversedList)

def derivationKeywordReplace(unlearDerivation):
    clearDeri = ""
    list = unlearDerivation.split(" ")
    for e in list:
        if e in LexemeDic.values():
            for key, value in LexemeDic.items():
                if e == value:
                    e = key
        clearDeri += e + " "
    return clearDeri

def derivationBuilder(newTransition, PrevDeriv):
    lhs, rhs = newTransition.split("→")
    if rhs.strip() == "&epsilon":
        rhs = ''
    newStr = PrevDeriv.replace(lhs.strip(),rhs.strip(),1)
    return newStr

def getFirstFollowInfo(token):
    isNullable = False
    isEndable = False
    firstSet = []
    followSet = []

    if isTerminal(token):
        firstSet.append(token)

    if token in FFTable.index.values: # valid nonterminal
        if FFTable["nullable"][token] == "yes":
            isNullable = True
        if FFTable["endable"][token] == "yes":
            isEndable = True
        firstSet = FFTable["first set"][token].split(" ")
        followSet = FFTable["follow set"][token].split(" ")
    return firstSet, followSet, isNullable, isEndable

def updateProdStack (prodStack, tableEntry):
    prodStack.pop()
    if tableEntry != "&epsilon ":
        seperatedList = tableEntry.split(' ')
        for word in seperatedList:
            if word != '':
                prodStack.append(word)

def buildAST():
    # popped = semanticStack.pop()
    # if popped != "/progSubtree/":
    #     return "Error"
    # while popped != "/eNode/":
    #     popped = semanticStack.pop()
    #     if popped == "/implSubtree/":
    #         while popped != "/eNode/":
    #             popped = semanticStack.pop()
    #         implDefNode()
    pass

def buildASTBuilder():

    if semanticStack[-1].endswith("Node/"):
        popped = semanticStack.pop()
        index = popped.index("Node")
        prefix = popped[1:index]
        test = getattr(Nodes, prefix)('my0', 0, 0)


    if semanticStack[-1].endswith("Subtree/"):
        popped = semanticStack.pop()
        while popped != "/eNode/":
            popped = semanticStack.pop()

        print(semanticStack[-1])



def parse(lexA):
    prodStack.append("START")
    prodStack.append("PROG")
    token = lexA.nextToken()
    while token.type == "inlinecmt" or token.type == "blockcmt":
        token = lexA.nextToken()
    success = True
    deriviation = "PROG"
    progDerivation = []
    errorList = []
    progDerivation.append(deriviation)

    while prodStack[-1] != "START":
        top = prodStack[-1]
        if isTerminal(top):
            if top == token.type:
                deleted = prodStack.pop()
                # if deleted == "id":  # replaced ID with the actual lexme in the derivation
                #     deriviation = deriviation.replace(" id ", " " + token.lexeme + " ", 1)
                previousToken = token
                token = lexA.nextToken()
                while token.type == "inlinecmt" or token.type == "blockcmt":
                    token = lexA.nextToken()
                # print("\nnewToken",token)
            else:
                while token.type == "inlinecmt" or token.type == "blockcmt":
                    token = lexA.nextToken()
                # ------ SKIP ERROR --------
                print("1syntax error at: " + str(token.location))
                errorList.append("syntax error at: " + str(token.location))
                firstSet, followSet, isNullable, isEndable = getFirstFollowInfo(top)
                if token.type == "eof" or token.type in followSet:
                    prodStack.pop()
                else:
                    while True:
                        token = lexA.nextToken()
                        if (token.type in firstSet) or (isNullable and token.type in followSet):
                            break
                # --------------------------
                success = False
        else:
            if top[-1] == '/':
                popped = prodStack.pop()

                if popped == "/e/":
                    semanticStack.append(popped)

                if popped.endswith("Node/"):
                    newNode = getattr(Nodes, popped[1:-1])(previousToken)
                    semanticStack.append(newNode)
                    print(newNode.token)

                if popped.endswith("Subtree/"):
                    poppedNode = semanticStack.pop()


                    if popped == ("/relOpSubtree/") or popped == ("/mulOpSubtree/") or popped == ("/addOpSubtree/"):
                        poppedNode2 = semanticStack.pop()
                        poppedNode3 = semanticStack.pop()

                        children = (poppedNode, poppedNode2, poppedNode3, )
                        newNode = getattr(Nodes, popped[1:-1])(tuple(reversed(children)))

                        semanticStack.append(newNode)

                        for pre, fill, node in RenderTree(newNode):
                            if node.name == "id" or node.name == "num" or node.name == "sign" or node.name.endswith("Op"):
                                print("%s%s: %s" % (pre, node.name, node.token.lexeme))
                            else:
                                print("%s%s" % (pre, node.name))

                    elif popped == ("/varSubtree/") or popped == ("/dotSubtree/") or popped == ("/funCallSubtree/") or popped == ("/assignSubtree/"):
                        poppedNode2 = semanticStack.pop()

                        children = (poppedNode, poppedNode2,)
                        newNode = getattr(Nodes, popped[1:-1])(tuple(reversed(children)))

                        semanticStack.append(newNode)

                        for pre, fill, node in RenderTree(newNode):
                            if node.name == "id" or node.name == "num" or node.name == "sign" or node.name.endswith(
                                    "Op"):
                                print("%s%s: %s" % (pre, node.name, node.token.lexeme))
                            else:
                                print("%s%s" % (pre, node.name))

                    elif popped == ("/progSubtree/"):
                        structDecList = ()
                        implDefList = ()
                        funcDefList = ()
                        while poppedNode != '/e/':
                            if poppedNode.name == "structDec":
                                structDecList += (poppedNode,)
                            if poppedNode.name == "implDef":
                                implDefList += (poppedNode,)
                            if poppedNode.name == "funcDef":
                                funcDefList += (poppedNode,)
                            poppedNode = semanticStack.pop()

                        structDecListNode = (getattr(Nodes, "structDecListSubtree")(tuple(reversed(structDecList))))
                        implDefListNode = (getattr(Nodes, "implDefListSubtree")(tuple(reversed(implDefList))))
                        funcDefListNode = (getattr(Nodes, "funcDefListSubtree")(tuple(reversed(funcDefList))))

                        children = (structDecListNode,implDefListNode,funcDefListNode,)
                        newNode = getattr(Nodes, popped[1:-1])(tuple(children))

                        semanticStack.append(newNode)
                        for pre, fill, node in RenderTree(newNode):
                            if node.name == "id" or node.name == "num" or node.name == "sign" or node.name.endswith(
                                    "Op"):
                                print("%s%s: %s" % (pre, node.name, node.token.lexeme))
                            else:
                                print("%s%s" % (pre, node.name))
                    else:
                        children = ()
                        while poppedNode != '/e/':
                            children += (poppedNode,)
                            poppedNode = semanticStack.pop()
                        newNode = getattr(Nodes, popped[1:-1])(tuple(reversed(children)))
                        semanticStack.append(newNode)
                        for pre, fill, node in RenderTree(newNode):
                            if node.name == "id" or node.name == "num" or node.name == "sign" or node.name.endswith(
                                    "Op"):
                                print("%s%s: %s" % (pre, node.name, node.token.lexeme))
                            else:
                                print("%s%s" % (pre, node.name))

                # semanticStack.append(popped)
                print(semanticStack)

                continue


            tableEntry, deriviation = getTableReversedRHS(top,token,deriviation)
            progDerivation.append(deriviation)

            if tableEntry != "0":
                updateProdStack(prodStack, tableEntry) # adds new RHS to the stack

            else:
                # ------ SKIP ERROR --------
                print("2syntax error at: " + str(token.location))
                errorList.append("syntax error at: " + str(token.location))
                firstSet, followSet, isNullable, isEndable = getFirstFollowInfo(top)
                if token.type == "eof" or token.type in followSet:
                    prodStack.pop()
                else:
                    while True:
                        token = lexA.nextToken()
                        if (token.type in firstSet) or (isNullable and token.type in followSet):
                            break
                # --------------------------
                success = False

    if (prodStack[-1] != "START") or (success == False):
        return False, progDerivation, errorList
    else:
        # for pre, fill, node in RenderTree(semanticStack.pop()):
        #     print("%s%s" % (pre, node.name))
        return True, progDerivation, errorList


