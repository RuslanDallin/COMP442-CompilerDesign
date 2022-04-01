from Visitor import *

class TypeCheckingVisitor(Visitor):
    def visit(self, node):

        # symTable = node.symTable
        # for child in node.children:
        #     child.symTable = symTable

        # node.base


        if type(node) is progSubtree: pass


        if type(node) is implDefSubtree: pass

        if type(node) is structDecSubtree: pass

        if type(node) is funcDefSubtree: pass

        if type(node) is memberDeclSubtree: pass

        if type(node) is funcDeclSubtree: pass

        if type(node) is varDeclSubtree:
            typeV = node.children[1]
            if typeV.data == "integer" or typeV.data == "float":
                pass
            else:
                if typeV.data not in self.getClassNames(node):
                    error = "undeclared class " + str(typeV.token.location)
                    ErrorList.append(error)


        if type(node) is Node: pass

        if type(node) is IdNode: pass

        if type(node) is MulOpNode: pass

        if type(node) is aParamsSubtree: pass

        if type(node) is addOpNode: pass

        if type(node) is addOpSubtree: pass

        if type(node) is assignSubtree: pass

        if type(node) is dimListSubtree: pass

        if type(node) is dotSubtree:
            leftChild = node.children[0]
            if leftChild.__class__.__name__ == "varSubtree":
                varID = leftChild.children[0]
                if varID not in self.getClassNames(node):
                    error = "operator used on non-class type " + str(varID.token.location)
                    ErrorList.append(error)

        if type(node) is factorSubtree: pass

        if type(node) is floatNode: pass

        if type(node) is fparmListSubtree: pass

        if type(node) is funCallSubtree: pass

        if type(node) is funcBodySubtree: pass

        if type(node) is funcDefListSubtree: pass

        if type(node) is funcDefSubtree: pass

        if type(node) is ifThenElseSubtree: pass

        if type(node) is implDefListSubtree: pass

        if type(node) is indiceListSubtree: pass
            # factors = node.children
            # if factors:
            #     for factor in factors:
            #         print(factor.children[0].__class__.__name__)
            #         # if factor.children[0].__class__.__name__.endswith("Node"):
            #         #     print(factor.children[0].data)


        if type(node) is inherListSubtree: pass

        if type(node) is memberDeclListSubtree: pass

        if type(node) is mulOpSubtree: pass

        if type(node) is numNode: pass

        if type(node) is readSubtree: pass

        if type(node) is relExprSubtree: pass

        if type(node) is relOpNode: pass

        if type(node) is relOpSubtree: pass

        if type(node) is returnSubtree: pass

        if type(node) is signNode: pass

        if type(node) is statSubtree: pass

        if type(node) is structDecListSubtree: pass

        if type(node) is typeNode: pass

        if type(node) is varSubtree: pass

        if type(node) is visibilityNode: pass

        if type(node) is whileSubtree: pass

        if type(node) is writeSubtree: pass