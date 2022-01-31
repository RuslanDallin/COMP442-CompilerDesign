import pandas as pd

table = pd.read_csv("Table.csv")
table.set_index("State", inplace=True)

LexemeDic = {"==": "eq", "+": "plus", "(": "openpar", ";": "semi", "<>": "noteq", "-": "minus",
             "&": "and", ")": "closepar", ",": "comma", "<": "lt", "*": "multi", "!": "not", "{": "opencubr",
             ".": "dot", ">": "gt", "/": "div", "}": "closecubr", ":": "colon", "<=": "leq", "=": "assign",
             "[": "opensqbr", "::": "coloncplon", ">=": "geg", "]": "closesqbr", "->": "arrow"}

reservedWords = ["if", "then", "else", "integer", "float", "void", "public", "private", "func", "var",
                 "struct", "while", "func", "read", "write", "return", "self", "inherits", "let", "impl"]

class Token:
    def __init__(self, label, token, location):
        token = token.lower()
        self.type = getTokenType(label, token)
        self.lexeme = token
        self.location = location

    def __str__(self):
        return "[%s, %s, %s]" % (self.type, self.lexeme, self.location)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.type == other.type and self.lexeme == other.lexeme
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

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


class Lex:
    lineCounter = 1
    def __init__(self, src):
        self.src = src

    def nextToken(self):
        state = 'A'
        lexeme = ""
        nextState = ''
        tokenReady = False
        token = None
        tokenLimit = 10
        while (token == None):
            char = self.src.read(1)

            if char == '\n':
                self.lineCounter += 1


            if tokenReady:
                tokenLimit -= 1

            if not char:  #reached end of file
                if tokenReady:
                    token = Token(nextLabel(nextState), lexeme, self.lineCounter - 1)
                    continue
                break

            if char == '\n' and tokenReady:  # if we reach the end of a line and we already have a valid token
                token = Token(nextLabel(nextState), lexeme, self.lineCounter-1)
                continue

            if char.isspace():
                if tokenReady and state != 'Z' and state != 'AA':  # if we reach the end of a line and we already have a valid token
                    token = Token(nextLabel(nextState), lexeme, self.lineCounter)
                continue

            nextState, label = getInfo(state, typeOfChar(state, char))

            if state == 'Z':  # inline comments end at \n
                while (char != '\n'):
                    lexeme += char
                    char = self.src.read(1)
                    if not char:
                        break
                token = Token("inlinecmt", repr(lexeme), self.lineCounter)
                self.lineCounter += 1
                continue

            if nextState == "AA":  # line block comments
                countOpen = 1
                countClosed = 0
                lexeme += char
                CommentStartLocation = self.lineCounter
                while (True):
                    char = self.src.read(1)
                    if char == '\n':
                        self.lineCounter += 1

                    if char == '/':
                        nextChar = self.src.read(1)
                        if nextChar == '*':
                            countOpen += 1
                        if nextChar != '\n':
                            lexeme += char + nextChar
                        continue

                    if char == '*':
                        nextChar = self.src.read(1)
                        if nextChar == '/':
                            countClosed += 1
                        if nextChar != '\n':
                            lexeme += char + nextChar
                        continue

                    if countOpen == countClosed:
                        break

                    if not char: #reached end of file
                        return Token("blockCommentMissing" + str(countOpen - countClosed) + "'*/'", repr(lexeme), self.lineCounter)

                    lexeme += char
                token = Token("blockcmt", repr(lexeme), CommentStartLocation)
                continue

            if nextState == "-1" and label == "-1":  # invalid char
                if char == '\n':
                    continue
                token = Token("invalidToken", char, self.lineCounter)
                continue

            if nextState == "0" and label == "0":  # misplaced char
                if char == '\n':
                    continue
                token = Token("misplacedToken", char, self.lineCounter)
                continue

            if (nextState == "0" and label != "0") or (label == "id" and lexeme in reservedWords):  # complete token and final state
                self.src.seek(self.src.tell() - 1)  # backtrack
                token = Token(label, lexeme, self.lineCounter)
                continue

            if state != "AA" and nextLabel(nextState) != "0":  # token is read in case next char is \n Token needs to be in final state
                tokenReady = True

            lexeme = lexeme + char
            state = nextState

        return token


