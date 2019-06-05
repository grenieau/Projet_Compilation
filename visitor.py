from ast import *

class Visitor:

    def __init__(self):
        self.indentation = 0
        self.Liste_variable = []
        self.nb_eqs = 0

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
            self.nb_eqs += 1 #comptage du nombre d'équations

    def visitEquation(self,equa,args):
        print('visitEquation')
        print('visitEquationLeft')
        i = 0 #parcourrir la liste des operateurs
        for left in equa.left.list_expr:
            left.accept(self,args)
            if i < len(equa.left.list_operateur):
                print(equa.left.list_operateur[i])
                i += 1

        print('visitEquationRight')
        i = 0
        for right in equa.right.list_expr:
            right.accept(self,args)
            if i < len(equa.right.list_operateur):
                print(equa.right.list_operateur[i])
                i += 1

    def visitRelation(self, rel, args):
        print('visitRelation')
        print('visitRelationLeft')
        i = 0
        for left in rel.list_expr:
            left.accept(self,args)
            if i < len(rel.list_operateur):
                print(rel.list_operateur[i])
                i += 1

    def visitInt(self, int, args):
        print("visitInt")
        print(int)

    def visitIdentifier(self, id, args):
        print("visitIdentifier")
        c = True
        for x in self.Liste_variable:
            if id.ident == x.ident:
                c = False
                break
        if c:
            self.Liste_variable.append(id)
            print(id)

    def solveSystem(self,parser):
        if self.nb_eqs < len(self.Liste_variable):
            print("Systeme non solvable, pas assez d'equations")
        elif self.nb_eqs == len(self.Liste_variable):
            print("Systeme solvable, nombre d'equation egal au nombre de variable")
            # Test pour savoir si le systeme est lineaire
            if parser.check_linear():
                print("Le systeme est lineaire")
                
        else:
            print("Systeme solvable par la méthode des moindres carres")
            # Test pour savoir si le systeme est lineaire
            if parser.check_linear():
                print("Le systeme est lineaire")
            
