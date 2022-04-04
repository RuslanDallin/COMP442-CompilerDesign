import os

from anytree import RenderTree

from CodeGeneration import *
from ComputeMemSizeVisitor import *
from LexicalAnalyzer import Lex
from Parser import parse
from SymTableVisitor import *
from TypeCheckingVisitor import *


from Visitor import *

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
                print("START =>" + deriv)
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
                if node.__class__.__name__.endswith("Node"):
                    astOutput.write(str(("%s%s: %s" % (pre, node.name, node.data))))
                    print("%s%s: %s" % (pre, node.name, node.data))
                else:
                    print("%s%s" % (pre, node.name))
                    astOutput.write(str("%s%s\n" % (pre, node.name)))

            print(parseCheck)
    # ---------------------------------------------------------------------


def visitorDriver():
    # TO BE DELETED -----------------------------------------------------
    directoryName = "Input"  # set the source folder
    directory = os.listdir(directoryName)
    for file in directory:
        filename = os.fsdecode(file)
        if file.endswith(".src"):  # go through all .src files
            SourceFileName = filename[0:-4]
            src = open(directoryName + "/" + SourceFileName + ".src", 'r')  # reading
            tableOutput = open("Output/" + SourceFileName + ".outsymboltables", 'w')  # symTable
            errosOutput = open("Output/" + SourceFileName + ".outsemanticerrors", 'w')  # symTable
            print("\n\n********* %s *********" % (SourceFileName))
            lex = Lex(src)
            parseCheck, deriviations, errors, ast = parse(lex)


            for pre, fill, node in RenderTree(ast):
                if node.__class__.__name__.endswith("Node"):
                    print("%s%s: %s" % (pre, node.name, node.data))
                else:
                    print("%s%s" % (pre, node.name))


            symTable = SymTableVisitor()
            ast.accept(symTable)

            # typeCheckingVisitor = TypeCheckingVisitor()
            # ast.accept(typeCheckingVisitor, ast.symTable)

            computeMemSize = ComputeMemSizeVisitor()
            ast.accept(computeMemSize, ast.symTable)

            CodeGeneration = CodeGenerationVisitor()
            ast.accept(CodeGeneration, ast.symTable)

            # print(ast.symTable)
            # tableOutput.write(str(ast.symTable))


            for error in ErrorList:
                print(error)
                errosOutput.write(str(error))
                errosOutput.write("\n")

    # ---------------------------------------------------------------------

# lexDriver()
# parserDriver()
# astDriver()
visitorDriver()