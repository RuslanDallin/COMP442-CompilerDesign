import os
import pandas as pd
from LexicalAnalyzer import *


# ParseTable = pd.read_csv("testTable.csv")
ParseTable = pd.read_csv("ParsingTable.csv")
ParseTable.set_index("TT", inplace=True)
prodStack = []
deletedStack = []


def isTerminal(s):
    return (s in LexemeDic.values()) or (s in reservedWords) or (s == "id")

        #TO BE DELELED
# def isTerminalTemp(s):
#     return s in ['0', '1', '(', ")", "+", "*", "eof"]
        #TO BE DELELED

def getTableReversedRHS(row,col,PrevDeriv):
    rhs= -1  # -1: no column match
    newDeriv = PrevDeriv
    if col in ParseTable.columns:
        rhs = str(ParseTable[col][row])
        if rhs == "nan":
            rhs = 0  # 0: cell is empty
        else:
            newDeriv = derivationBuilder(clearDerivation(rhs),PrevDeriv)
            arrowIndex = rhs.index("→ ") + 2
            trucatedRhs = rhs[arrowIndex:]
            rhs = reverseSentence(trucatedRhs) + " "

    print("[row: ", row,"] - [col (token): ", col,"] - [result: ", rhs, "] - [Terminal:", isTerminal(col),"]")
    return str(rhs), newDeriv

def reverseSentence(s):
    tempList = s.split()
    reversedList = reversed(tempList)
    return " ".join(reversedList)

def clearDerivation(unlearDerivation):
    clearDeri = ""
    list = unlearDerivation.split(" ")
    for e in list:
        if e in LexemeDic.values():
            for key, value in LexemeDic.items():
                if e == value:
                    e = key
        clearDeri += e + " "
    return clearDeri

def derivationBuilder(s, PrevDeriv):
    lhs, rhs = s.split("→")
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
    deriviationList = []
    errorList = []
    deriviationList.append(deriviation)
    print("START =>", deriviation)

    while prodStack[-1] != "START": # CHANGE TO START
        # print(prodStack)
        top = prodStack[-1]
        if isTerminal(top):
            print(top," == ", token.type,"?", top == token.type)
            if top == token.type:
                print("\n")
                print(prodStack)
                deleted = prodStack.pop()
                print(deleted, " deleted ------")
                print(prodStack)
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
            tableEntry, deriviation = getTableReversedRHS(top,token.type,deriviation)
            print("\nSTART =>", deriviation)
            deriviationList.append(deriviation)
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
        return False, deriviationList, errorList
    else:
        return True, deriviationList, errorList


