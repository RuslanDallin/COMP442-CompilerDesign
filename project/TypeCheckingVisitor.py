from Visitor import *

class TypeCheckingVisitor(Visitor):
    def visit(self, node):

        if type(node) is progSubtree: pass

        if type(node) is implDefSubtree: pass

        if type(node) is structDecSubtree: pass

        if type(node) is funcDefSubtree: pass

        if type(node) is memberDeclSubtree: pass

        if type(node) is funcDeclSubtree: pass

        if type(node) is varDeclSubtree: pass

        if type(node) is Node: pass

        if type(node) is IdNode: pass

        if type(node) is MulOpNode: pass

        if type(node) is aParamsSubtree: pass

        if type(node) is addOpNode: pass

        if type(node) is addOpSubtree: pass

        if type(node) is assignSubtree: pass

        if type(node) is dimListSubtree: pass

        if type(node) is dotSubtree: pass

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