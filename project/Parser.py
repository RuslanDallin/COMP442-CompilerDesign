import pandas as pd
from LexicalAnalyzer import Lex

table = pd.read_csv("ParsingTable.csv")
table.set_index("TT", inplace=True)

prodStack = []

def parse():
    prodStack.push("$")
    prodStack.push("START")
    Lex.nextToken()
    while prodStack[-1] != "$":
        top = prodStack[-1]
        if top