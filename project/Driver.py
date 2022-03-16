import os

from anytree import RenderTree

from LexicalAnalyzer import Lex
from Parser import parse

directoryName = "Input" # set the source folder
directory = os.listdir(directoryName)

def lexDriver():
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

def parserDriver():
    # TO BE DELETED -----------------------------------------------------
    directoryName = "Input"  # set the source folder
    directory = os.listdir(directoryName)
    for file in directory:
        filename = os.fsdecode(file)
        if file.endswith(".src"):  # go through all .src files
            SourceFileName = filename[0:-4]
            src = open(directoryName + "/" + SourceFileName + ".src", 'r')  # reading
            outderivation = open("Output/" + SourceFileName + ".outderivation", 'w')  # tokens
            outsyntaxerrors = open("Output/" + SourceFileName + ".outsyntaxerrors", 'w')  # errors
            astOutput = open("Output/" + SourceFileName + ".outast", 'w')  # ast tree
            print("\n\n********* %s *********" % (SourceFileName))
            lex = Lex(src)
            parseCheck, deriviations, errors, ast = parse(lex)
            for deriv in deriviations:
                # print("START =>", deriv)
                outderivation.write("START =>" + deriv + "\n")
            for error in errors:
                outsyntaxerrors.write(error + "\n")
            print(parseCheck)
    # ---------------------------------------------------------------------

def astDriver():
    # TO BE DELETED -----------------------------------------------------
    directoryName = "Input"  # set the source folder
    directory = os.listdir(directoryName)
    for file in directory:
        filename = os.fsdecode(file)
        if file.endswith(".src"):  # go through all .src files
            SourceFileName = filename[0:-4]
            src = open(directoryName + "/" + SourceFileName + ".src", 'r')  # reading
            astOutput = open("Output/" + SourceFileName + ".outast", 'w')  # ast tree
            print("\n\n********* %s *********" % (SourceFileName))
            lex = Lex(src)
            parseCheck, deriviations, errors, ast = parse(lex)
            for pre, fill, node in RenderTree(ast):
                if node.name == "id" or node.name == "num" or node.name == "float" \
                        or node.name == "sign" or node.name == "type" \
                        or node.name == "visibility" or node.name.endswith("Op"):
                    astOutput.write(str("%s%s: %s\n" % (pre, node.name, node.token.lexeme)))
                else:
                    astOutput.write(str("%s%s\n" % (pre, node.name)))

            for pre, fill, node in RenderTree(ast):
                if node.name == "id" or node.name == "num" or node.name == "float" \
                        or node.name == "sign" or node.name == "type" \
                        or node.name == "visibility" or node.name.endswith("Op"):
                    print("%s%s: %s" % (pre, node.name, node.token.lexeme))
                else:
                    print("%s%s" % (pre, node.name))

            print(parseCheck)
    # ---------------------------------------------------------------------

# lexDriver()
# parserDriver()
# astDriver()