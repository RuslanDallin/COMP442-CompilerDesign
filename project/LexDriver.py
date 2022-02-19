import os
from LexicalAnalyzer import Lex

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
        temp = lex.nextToken()
        lineNumber = 1
        print("\n\n********* %s *********" % (SourceFileName))
        while (temp.type != "eof"):
            if temp.location != lineNumber:
                print("")
                outlextokens.write("\n")
            print(temp, end="")
            outlextokens.write(temp.__str__())
            if temp.type == "invalidToken":
                outlexerrors.write("Lexical error: Invalid character: \"%s\": line %s.\n" % (temp.lexeme, temp.location))
            if temp.type == "misplacedToken":
                outlexerrors.write("Lexical error: Misplaced character: \"%s\": line %s.\n" % (temp.lexeme, temp.location))
            if temp.type.startswith("blockCommentMissing"):
                outlexerrors.write("Lexical error: Missing closing " + temp.type[19] + " */: \"%s\": line %s.\n" % (temp.lexeme, temp.location))
            lineNumber = temp.location
            temp = lex.nextToken()
        src.close()
        outlexerrors.close()
        outlextokens.close()
