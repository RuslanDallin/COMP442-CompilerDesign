import os
from LexicalAnalyzer import Lex

directory = os.fsencode("./")
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith(".src"):
        SourceFileName = filename[0:-4]
        src = open(SourceFileName + ".src", 'r')  # reading
        outlextokens = open(SourceFileName + ".outlextokens", 'w')  # tokens
        outlexerrors = open(SourceFileName + ".outlexerrors", 'w')  # errors
        lex = Lex(src)
        temp = lex.nextToken()
        lineNumber = 1
        while (temp != None):
            print(temp)
            if temp.location != lineNumber:
                outlextokens.write("\n")
            outlextokens.write(temp.__str__())
            if temp.type == "invalidToken":
                outlexerrors.write("Lexical error: Invalid character: \"%s\": line %s.\n" % (temp.lexeme, temp.location))
            if temp.type == "misplacedToken":
                outlexerrors.write("Lexical error: misplaced character: \"%s\": line %s.\n" % (temp.lexeme, temp.location))
            lineNumber = temp.location
            temp = lex.nextToken()
        src.close()
        outlexerrors.close()
        outlextokens.close()
