import pandas as pd

table = pd.read_csv("Table.csv")
table.set_index("State", inplace=True)

SourceFileName = "lexpositivegrading"
src = open(SourceFileName + ".src", 'r') # reading
outlextokens = open(SourceFileName + ".outlextokens", 'w') # tokens
outlexerrors = open(SourceFileName + ".outlexerrors", 'w') # errors


LexemeDic = {"==": "eq", "+": "plus", "(": "openpar", ";": "semi", "<>": "noteq", "-": "minus",
             "&": "and", ")": "closepar", ",": "comma", "<": "lt", "*": "multi", "!": "not", "{": "opencubr",
             ".": "dot", ">": "gt", "/": "div", "}": "closecubr", ":": "colon", "<=": "leq", "=": "assign",
             "[": "opensqbr", "::": "coloncplon", ">=": "geg", "]": "closesqbr", "->": "arrow"}

reservedWords = ["if", "then", "else", "integer", "float", "void", "public", "private", "func", "var",
                 "struct", "while", "func", "read", "write", "return", "self", "inherits", "let", "impl"]


class Token:
    def __init__(self, label, token, location, index):
        tempType = LexemeDic.get(type)
        if tempType == None:
            tempType = type
        self.type = getTokenType(label, token)
        self.lexeme = token
        self.location = location
        self.index = index

    def __str__(self):
        return "[%s, %s, %s, %s]" % (self.type, self.lexeme, self.location, self.index)

    def __eq__(self, other):
        return self.type == other.type and self.lexeme == other.lexeme


def typeOfChar(state, c):
    if c == '0':  # special case 1. 0 should be treated as 0 and not a digit
        if state == 'A' or state == 'AR' or state == 'AT'or state == 'AB' or state == 'AU': # these states have '0' transitions
            return '0'
    if c == 'e':  # special case 2. e should be treated as e and not a letter
        if state == 'AR' or state == 'AP': # these states have '0' transitions
            return 'e'
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

def getTokenType(label, token):
    tempType = LexemeDic.get(token)
    if tempType != None: # operator
        return tempType
    if token in reservedWords: # reserved word
        return token
    return label


def nextLabel(state):
    tempLabel = str(table["final"][state])
    if tempLabel == "nan":
        tempLabel = 0  # not a final state
    return str(tempLabel)


def nextToken():
    while True:
        state = 'A'
        token = ""
        label = None
        nextState = ""
        tokenReady = False
        typeChar = ''
        lineCounter = 1
        while (True):
            char = src.read(1)

            if char == '\n':
                lineCounter += 1

            if not char:  #reached end of file
                if tokenReady:
                    print(Token(nextLabel(nextState), token, lineCounter - 1, src.tell()))
                    state = 'A'
                    token = ""
                    tokenReady = False
                return

            if char.isspace() and char != '\n':  # we only care of newlines
                continue

            if char == '\n' and tokenReady:  # if we reach the end of a line and we already have a valid token
                print(Token(nextLabel(nextState), token, lineCounter-1, src.tell()))
                state = 'A'
                token = ""
                tokenReady = False
                continue

            nextState, label = getInfo(state, typeOfChar(state, char))

            if state == 'Z':  # inline comments end at \n
                while (char != '\n'):
                    token += char
                    char = src.read(1)
                # print(char, typeChar, nextState, label)
                print(Token("inlinecmt", repr(token), lineCounter, src.tell()))
                state = 'A'
                token = ""
                tokenReady = False
                lineCounter += 1
                continue

            if nextState == "AA":  # line block comments
                countOpen = 1
                countClosed = 0
                token += char
                CommentStartLocation = lineCounter
                while (True):
                    char = src.read(1)
                    if char == '\n':
                        lineCounter += 1

                    if char == '/':
                        nextChar = src.read(1)
                        if nextChar == '*':
                            countOpen += 1
                        if nextChar != '\n':
                            token += char + nextChar
                        continue

                    if char == '*':
                        nextChar = src.read(1)
                        if nextChar == '/':
                            countClosed += 1
                        if nextChar != '\n':
                            token += char + nextChar
                        continue

                    if countOpen == countClosed:
                        break

                    if not char: #reached end of file
                        print(Token("blockCommentMissing" + str(countOpen - countClosed) + "'*/'", repr(token), lineCounter, src.tell()))
                        return

                    token += char
                # print(char, typeChar, nextState, label)
                print(Token("blockcmt", repr(token), CommentStartLocation, src.tell()))
                state = 'A'
                token = ""
                tokenReady = False
                continue

            if nextState == "-1" and label == "-1":  # invalid char
                if char == '\n':
                    continue
                # print("@INVALID Token", repr(char))
                print(Token("invalidToken", char, lineCounter, src.tell()))
                continue

            if nextState == "0" and label == "0":  # misplaced char
                if char == '\n':
                    continue
                # print("#INVALID Token", repr(char))
                print(Token("misplacedToken", char, lineCounter, src.tell()))
                continue

            if (nextState == "0" and label != "0") or (label == "id" and token in reservedWords):  # complete token and final state
                # print(char, typeChar, nextState, label)
                print(Token(label, token, lineCounter, src.tell()))
                state = 'A'
                token = ""
                src.seek(src.tell() - 1)  # backtrack
                tokenReady = False
                continue

            if state != "AA" and nextLabel(nextState) != "0":  # token is read in case next char is \n Token needs to be in final state
                tokenReady = True

            token = token + char
            state = nextState
            # print(char, typeChar, nextState, label)


print(nextToken())
