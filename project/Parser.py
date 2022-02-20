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
            newDeriv = derivationBuilder(rhs,PrevDeriv)
            arrowIndex = rhs.index("→ ") + 2
            trucatedRhs = rhs[arrowIndex:]
            rhs = reverseSentence(trucatedRhs) + " "

    print("[row: ", row,"] - [col (token): ", col,"] - [result: ", rhs, "] - [Terminal:", isTerminal(col),"]")
    return str(rhs), newDeriv

def reverseSentence(s):
    tempList = s.split()
    reversedList = reversed(tempList)
    return " ".join(reversedList)

def derivationBuilder(s, PrevDeriv):
    lhs, rhs = s.split("→")
    if rhs.strip() == "&epsilon":
        rhs = ''
    PrevDeriv = PrevDeriv.replace(lhs.strip(),rhs.strip(),1)
    # newStr = PrevDeriv.replace(" ", "")
    newStr = PrevDeriv
    return newStr


def parse(lexA):
    prodStack.append("START")
    prodStack.append("PROG")
    token = lexA.nextToken()
    error = False
    deriviation = "PROG"
    print("START =>", deriviation)

    while prodStack[-1] != "START": # CHANGE TO START
        # print(prodStack)
        top = prodStack[-1]
        if isTerminal(top):
            print(top," == ", token.type,"?", top == token.type)
            if top == token.type:
                deleted = prodStack.pop()
                print(deleted, " deleted ------")
                token = lexA.nextToken()
                # print("\nnewToken",token)
            else:
                #skipErrors()
                token = lex.nextToken()
                error = True
                break
        else:
            tableEntry, deriviation = getTableReversedRHS(top,token.type,deriviation)
            print("\nSTART =>", deriviation)
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
        return False
    else:
        return True

# print(parse())
# print(reverseSentence("EXPR REPTAPARAMS1"))

# TO BE DELETED -----------------------------------------------------
directoryName = "Test" # set the source folder
directory = os.listdir(directoryName)
for file in directory:
    filename = os.fsdecode(file)
    if file.endswith(".src"): # go through all .src files
        SourceFileName = filename[0:-4]
        src = open(directoryName + "/" + SourceFileName + ".src", 'r')  # reading
        outlextokens = open("Output/" + SourceFileName + ".outlextokens", 'w')  # tokens
        outlexerrors = open("Output/" + SourceFileName + ".outlexerrors", 'w')  # errors
        lex = Lex(src)
        print(parse(lex))
# ---------------------------------------------------------------------


