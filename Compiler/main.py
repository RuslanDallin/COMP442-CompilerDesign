import math

import pandas as pd

table = pd.read_csv("table.csv")
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


def nextToken():
    while True:
        state = 'A'
        token = None
        label = None
        tokenReady = False
        while (token == None):
            char = file.read(1)
            if not char:
                return None
            if char == '' or char == '\t':
                continue
            newState = str(getState(state,type(char)))
            if newState.isalpha():
                state = newState
                newLabel = str(getLabel(state))
                if newLabel != 0:
                    label = newLabel
                    if tokenReady:
                        print(char, end="")
                        print(" ", state, label, tokenReady)
                        print("Token Created")
                        state = 'A'
                        token = None
                        label = None
                        tokenReady = False
                        continue
                    tokenReady = True
            elif newState == '0':
                print(char, end="")
                print(" ", state, label, tokenReady)
                print("Token Created")
                state = 'A'
                token = None
                label = None
                tokenReady = False
                file.seek(file.tell() -1) #go back
                continue

            print(char, end="")
            print(" ", state, label, tokenReady)





print(nextToken())