import pandas as pd

table = pd.read_csv("Table.csv")
table.set_index("State", inplace=True)
file = open('lexnegativegrading.src', 'r')


class Token:
    def __init__(self, type, lexeme, location):
        self.type = type
        self.lexeme = lexeme
        self.location = location


LexemeDic = {"==": "eq", "+": "plus", "(": "openpar", ";": "semi", "<>": "noteq", "-": "minus",
             "&": "and", ")": "closepar", ",": "comma", "<": "lt", "*": "multi", "!": "not", "{": "opencubr",
             ".": "dot", ">": "gt", "/": "div", "}": "closecubr", ":": "colon", "<=": "leq", "=": "assign",
             "[": "opensqbr", "::": "coloncplon", ">=": "geg", "]": "closesqbr", "->": "arrow", }

reservedWords = ["if", "then", "else", "integer", "float", "void", "public", "private", "func", "var",
                 "struct", "while", "func", "read", "write", "return", "self", "inherits", "let", "impl"]


def type(c):
    if c.isalpha(): return 'L'
    if c.isdigit() and c != '0': return 'N'
    if c.isdigit(): return 'D'
    return c


def getInfo(state, c):
    tempState = -1  # char not supported
    tempLabel = -1
    if c in table.columns:
        tempState = str(table[c][state])
        if tempState == "nan":
            tempState = 0  # no transations
        tempLabel = str(table["final"][state])
        if tempLabel == "nan":
            tempLabel = 0  # not a final state
    return str(tempState), str(tempLabel)


def isComplete(state):
    tempLabel = str(table["final"][state])
    if tempLabel == "nan":
        tempLabel = 0  # not a final state
    return str(tempLabel)


def nextToken():
    while True:
        state = 'A'
        token = ""
        label = None
        tokenReady = False
        typeChar = ''
        while (True):
            char = file.read(1)
            if not char:
                return None
            if char.isspace() and char != '\n':
                continue

            if char == '\n' and tokenReady:
                print("Token", token)
                state = 'A'
                token = ""
                tokenReady = False
                continue

            typeChar = type(char)
            if ((state == 'A' or state == 'AR' or state == 'AT') and char == '0') or (
                    state == 'AR' and char == 'e'):  # if there is a 0 with nothing around, it should be considered 0 not digit
                typeChar = char
            nextState, label = getInfo(state, typeChar)

            if state == 'Z':  # // comments
                while (char != '\n'):
                    token += char
                    char = file.read(1)
                print(char, typeChar, nextState, label)
                token = token + char
                print("Token", token)
                state = 'A'
                token = ""
                tokenReady = False

            if nextState == "AA":
                countOpen = 1
                countClosed = 0
                token += char
                while (True):
                    char = file.read(1)

                    if char == '/':
                        nextChar = file.read(1)
                        if nextChar == '*':
                            countOpen += 1
                        if nextChar != '\n':
                            token += char + nextChar
                        continue

                    if char == '*':
                        nextChar = file.read(1)
                        if nextChar == '/':
                            countClosed += 1
                        if nextChar != '\n':
                            token += char + nextChar
                        continue

                    if countOpen == countClosed:
                        break

                    token += char

                print(char, typeChar, nextState, label)
                token = token + char
                print("Token", repr(token))
                state = 'A'
                token = ""
                tokenReady = False
                continue

            if nextState == "-1" and label == "-1":
                if char == '\n':
                    continue
                print("@INVALID Token", repr(char))
                continue

            if nextState == "0" and label == "0":
                if char == '\n':
                    continue
                print("#INVALID Token", repr(char))
                continue

            if (nextState == "0" and label != "0") or (label == "id" and token in reservedWords):
                print(char, typeChar, nextState, label)
                print("Token", token)
                state = 'A'
                token = ""
                file.seek(file.tell() - 1)  # go back
                tokenReady = False
                continue

            if state != "AA" and isComplete(nextState) != "0":
                tokenReady = True

            token = token + char
            state = nextState
            print(char, typeChar, nextState, label)


print(nextToken())
