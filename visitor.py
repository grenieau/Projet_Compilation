from ast import *

class Visitor:

    def __init__(self):
        self.indentation = 0
        self.Liste_variable = []
    # definition des indentations
    def indent(self):
        self.indentation += 2

    def desindent(self):
        self.indentation -= 2

    # lancement du visiteur
    def doIt(self, ast):
        print("----------------------VISITOR----------------------")
        self.visitSysteme(ast,None)

    def visitSysteme(self, ast, args = None):
        print("visitSysteme")
        for eq in ast.equations:
            eq.accept(self,args)

    def visitEquation(self,equa,args):
        print('visitEquation')
        print('visitEquationLeft')

        for left in equa.left.list_expr:
            left.accept(self,args)
        for leftop in equa.left.list_operateur:
            print(leftop)

        print('visitEquationRight')
        for right in equa.right.list_expr:
            right.accept(self,args)
        for rightop in equa.right.list_operateur:
            print(rightop)

    def visitRelation(self, rel, args):
        print('visitRelation')
        print('visitRelationLeft')
        for left in rel.list_expr:
            left.accept(self,args)
        for leftop in rel.list_operateur:
            print(leftop)
        print('visitRelationLeft')
        for right in rel.list_expr:
            right.accept(self,args)
        for rightop in rel.list_operateur:
            print(rightop)


    def visitInt(self, int, args):
        print("visitInt")
        print(int)

    def visitIdentifier(self, id, args):
        print("visitIdentifier")
        print(id)
