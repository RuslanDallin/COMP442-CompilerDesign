import os

from anytree import RenderTree

from LexicalAnalyzer import Lex
from Parser import parse

directoryName = "Input" # set the source folder
directory = os.listdir(directoryName)

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
            print(parseCheck)
    # ---------------------------------------------------------------------

astDriver()
