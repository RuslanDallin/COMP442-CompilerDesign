import os
import pandas as pd
from LexicalAnalyzer import *


ParseTable = pd.read_csv("ParsingTable.csv")
ParseTable.set_index("TT", inplace=True)
prodStack = []


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

def parse(lexA):
    prodStack.append("START")
    prodStack.append("PROG")
    token = lexA.nextToken()
    while token.type == "inlinecmt" or token.type == "blockcmt":
        token = lexA.nextToken()
    error = False
    deriviation = "PROG"
    progDerivation = []
    errorList = []
    progDerivation.append(deriviation)

    while prodStack[-1] != "START":
        top = prodStack[-1]
        if isTerminal(top):
            if top == token.type:
                deleted = prodStack.pop()
                if deleted == "id": # replaced ID with the actual lexme in the derivation
                    deriviation = deriviation.replace("id", token.lexeme, 1)
                token = lexA.nextToken()
                while token.type == "inlinecmt" or token.type == "blockcmt":
                    token = lexA.nextToken()
                # print("\nnewToken",token)
            else:
                #skipErrors()
                while token.type == "inlinecmt" or token.type == "blockcmt":
                    token = lexA.nextToken()
                error = True
                break
        else:
            tableEntry, deriviation = getTableReversedRHS(top,token,deriviation)
            progDerivation.append(deriviation)
            if (tableEntry == "0"):
                print("\n--------------------------------")
                print("Error encoundered in the grammar")
                print("token: ", token)
                print("current stack: ", prodStack)
                errorList.append("syntax error at: " + str(token.location))
                print("--------------------------------")
                break
            if tableEntry != "-1":
                prodStack.pop()
                if tableEntry != "&epsilon ":
                    seperatedList = tableEntry.split(' ')
                    for word in seperatedList:
                        if word != '':
                            prodStack.append(word)
            else:
                error = True
                break

    if (prodStack[-1] != "START") or (error):
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


