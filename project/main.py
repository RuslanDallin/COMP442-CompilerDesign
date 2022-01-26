import math

import pandas as pd

table = pd.read_csv("Table.csv")
table.set_index("State", inplace=True)

file = open('lexpositivegrading.src', 'r')

def isLetter(c):
    return c.isalpha()

def isDigit(c):
    return c.isdigit()

def isNonZero(c):
    return c.isdigit() and c != '0'

# operators = ['!', '&', ',', '-', '.', '/', ':', ';', '<', '=', '>', '[', '|', ']', '_', '+', '.', '.', '.', '.', '.', '.',]

def type(c):
    if c.isalpha(): return 'L'
    if c.isdigit() and c != '0': return 'N'
    if c.isdigit(): return 'D'
    return c

def getState(state,c):
    if c in table.columns:
        temp = str(table[c][state])
        if temp == "nan":
            return 0 #no transitions
        else:
            return temp
    return -1  #symbol not supported

def getLabel(state):
    temp = str(table["final"][state])
    if temp == "nan":
        return 0 #no transitions
    else:
        return temp

def getInfo(state,c):
    tempState = -1  # char not supported
    tempLabel = -1
    if c in table.columns:
        tempState = str(table[c][state])
        if tempState == "nan":
            tempState = 0   # no transations
        tempLabel = str(table["final"][state])
        if tempLabel == "nan":
            tempLabel = 0   # not a final state
    return str(tempState), str(tempLabel)

def isComplete(state):
    tempLabel = str(table["final"][state])
    if tempLabel == "nan":
        tempLabel = 0  # not a final state
    return str(tempLabel)

reservedWords = ["if", "then", "else", "integer", "float", "void", "public", "private", "func", "var",
                 "struct", "while", "func", "read", "write", "return", "self", "inherits", "let", "impl"]

def nextToken():
    while True:
        state = 'A'
        token = ""
        label = None
        tokenReady = False
        typeChar = '0'
        while (True):
            char = file.read(1)
            if not char:
                return None
            if char == '' or char == '\t':
                continue

            if not (state == 'A' and char == '0'): # if there is a 0 with nothing around, it should be considered 0 not digit
                typeChar = type(char)
            nextState, label = getInfo(state,typeChar)


            if nextState == "-1" and label == "-1":
                continue

            if nextState == "0" and label == "0":
                continue

            if (nextState == "0" and label != "0") or (label == "id" and token in reservedWords):
                print(char, typeChar, nextState, label)
                print("Token",token)
                state = 'A'
                token = ""
                file.seek(file.tell() - 1)  # go back
                continue

            token = token + char
            state = nextState
            print(char, typeChar, nextState, label)








# def nextToken():
#     while True:
#         state = 'A'
#         token = ""
#         label = None
#         tokenReady = False
#         while (True):
#             char = file.read(1)
#             if not char:
#                 return None
#             if char == '' or char == '\t':
#                 continue
#             typeChar = type(char)
#             newState = str(getState(state,typeChar))
#             if newState.isalpha():
#                 state = newState
#                 newLabel = str(getLabel(state))
#                 if newLabel != 0:
#                     label = newLabel
#                     if tokenReady:
#                         # print(char, end="")
#                         # print(" ", state, label, tokenReady)
#                         # print("Token Created")
#                         # state = 'A'
#                         # token = None
#                         # label = None
#                         # tokenReady = False
#                         # continue
#                          pass
#                     tokenReady = True
#                     token = token + char
#
#             elif newState == '0':
#                 print(char, end="")
#                 print(" ", state, label, tokenReady)
#                 print("********Token Created",token)
#                 state = 'A'
#                 token = ""
#                 label = None
#                 tokenReady = False
#                 file.seek(file.tell() -1) #go back
#                 continue
#
#             print(char, end="")
#             print(" ", state, label, tokenReady)





print(nextToken())