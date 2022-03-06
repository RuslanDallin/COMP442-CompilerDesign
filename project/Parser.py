import os
import pandas as pd
from LexicalAnalyzer import *


ParseTable = pd.read_csv("parsing Test.csv")
ParseTable.set_index("TT", inplace=True)
FFTable = pd.read_csv("FF test.csv")
FFTable.set_index("nonterminal", inplace=True)

prodStack = []


def isTerminal(s):
    return s in ['opar', 'zero', '+', 'one', 'cpar', '*', '$']

def getTableReversedRHS(row,token,PrevDeriv):
    rhs= -1  # -1: no column match
    newDeriv = PrevDeriv
    col = token.lexeme
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

    if token in FFTable.index.values: # valid nonterminal
        if FFTable["nullable"][token] == "yes":
            isNullable = True
        if FFTable["endable"][token] == "yes":
            isEndable = True
        firstSet = FFTable["first set"][token].split(" ")
        followSet = FFTable["follow set"][token].split(" ")
    return firstSet, followSet, isNullable, isEndable

def parse(lexA):
    prodStack.append("$")
    prodStack.append("E")
    token = lexA.nextToken()
    while token.type == "inlinecmt" or token.type == "blockcmt":
        token = lexA.nextToken()
    success = True
    deriviation = "E"
    progDerivation = []
    errorList = []
    progDerivation.append(deriviation)

    while prodStack[-1] != "$":
        top = prodStack[-1]
        if isTerminal(top):
            if top == token.lexeme:
                deleted = prodStack.pop()
                if deleted == "id": # replaced ID with the actual lexme in the derivation
                    deriviation = deriviation.replace("id", token.lexeme, 1)
                token = lexA.nextToken()
                while token.type == "inlinecmt" or token.type == "blockcmt":
                    token = lexA.nextToken()
                # print("\nnewToken",token)
            else:
                while token.type == "inlinecmt" or token.type == "blockcmt":
                    token = lexA.nextToken()
                # ------ SKIP ERROR --------
                print("1syntax error at ", token.location)
                firstSet, followSet, isNullable, isEndable = getFirstFollowInfo(top)
                if token.lexeme == "eof" or token.lexeme in followSet:
                    prodStack.pop()
                else:
                    while (token.lexeme not in firstSet) or (isNullable and token.lexeme not in followSet):
                        firstSet, followSet, isNullable, isEndable = getFirstFollowInfo(top)
                        token = lexA.nextToken()
                # --------------------------
                success = False
                break
        else:
            tableEntry, deriviation = getTableReversedRHS(top,token,deriviation)
            progDerivation.append(deriviation)

            if tableEntry != "0":
                prodStack.pop()
                if tableEntry != "&epsilon ":
                    seperatedList = tableEntry.split(' ')
                    for word in seperatedList:
                        if word != '':
                            prodStack.append(word)
            else:
                # ------ SKIP ERROR --------
                print("2syntax error at ", token.location)
                firstSet, followSet, isNullable, isEndable = getFirstFollowInfo(top)
                if token.lexeme == "eof" or token.lexeme in followSet:
                    prodStack.pop()
                else:
                    while (token.lexeme not in firstSet) and (isNullable and token.lexeme not in followSet):
                        token = lexA.nextToken()
                # --------------------------
                success = False

    if (prodStack[-1] != "$") or (success == False):
        print("\n--------------------------------")
        print("Ended on ")
        print("token: ", token)
        print("current stack: ", prodStack)
        print("Col: ", top, "row: ", token.type, " tableEntry: ", tableEntry)
        errorList.append("syntax error at: " + str(token.location))
        print("--------------------------------")
        return False, progDerivation, errorList
    else:
        return True, progDerivation, errorList


