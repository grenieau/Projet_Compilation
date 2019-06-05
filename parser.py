import sys

from indent import Indent
from ast import *


class Parser:

    OP = ['ADD', 'SUB', 'MUL', 'DIV']
    EXPR = ['INTEGER_LIT','IDENTIFIER']

    def __init__(self, verbose=False):
        self.AST = None
        self.indentator = Indent(verbose)
        self.tokens = []
        self.errors = 0

    def show_next(self, n=1):
        try:
            return self.tokens[n - 1]
        except IndexError:
            print('ERROR: no more tokens left!')
            sys.exit(1)

    def expect(self, kind):
        actualToken = self.show_next()
        actualKind = actualToken.kind
        actualPosition = actualToken.position
        if actualKind == kind:
            return self.accept_it()
        else:
            print('Error at {}: expected {}, got {} instead'.format(str(actualPosition), kind, actualKind))
            sys.exit(1)

    # same as expect() but no error if not correct kind
    def maybe(self, kind):
        if self.show_next().kind == kind:
            return self.accept_it()

    def accept_it(self):
        token = self.show_next()
        output = str(token.kind) + ' ' + token.value
        self.indentator.say(output)
        return self.tokens.pop(0)

    def parse(self, tokens):
        self.tokens = tokens
        self.parse_program()

    def parse_program(self):
        self.indentator.indent('Parsing Program')

        self.expect('SYSTEME')
        self.AST = Systeme()
        self.expect('LBRACE')
        self.parse_declarations()
        self.expect('RBRACE')
        self.indentator.dedent()
        if (self.errors == 1):
            print('WARNING: 1 error found!')
        elif (self.errors > 1):
            print('WARNING: ' + str(self.errors) + ' errors found!')
        else:
            print('parser: syntax analysis successful!')

    def parse_declarations(self):
        self.indentator.indent('Parsing Declarations')
        actualToken = self.show_next()
        actualKind = actualToken.kind
        while actualKind != 'RBRACE':
            self.AST.equations.append(Equation()) #Ajout D'une Equation
            self.parse_declaration()
            actualToken = self.show_next()
            actualKind = actualToken.kind
        self.indentator.dedent()

    def parse_declaration(self):
        if self.show_next().kind == 'RBRACE':
            return()
        self.parse_membreGauche()
        self.expect('ASSIGN')
        self.parse_assignment()

    def parse_membreGauche(self):
        self.AST.equations[-1].left = Relation() #Ajout d'un relation
        actualToken = self.show_next()
        actualKind = actualToken.kind
        if actualKind == 'SUB':
            self.accept_it()
            for kind in Parser.EXPR:
                if self.show_next().kind == kind:

                    if kind == 'INTEGER_LIT':
                        self.AST.equations[-1].left.list_expr.append(Int(-int(self.show_next().value)))
                    if kind == 'IDENTIFIER':
                        self.AST.equations[-1].left.list_expr.append(Identifier(self.show_next().value, True))
                    self.expect(kind)

        while self.show_next().kind != 'ASSIGN':
            self.parse_expression(self.AST.equations[-1].left)


    def parse_assignment(self):
        actualToken = self.show_next()
        actualKind = actualToken.kind
        self.AST.equations[-1].right = Relation()
        if actualKind == 'SUB':
            self.accept_it()
            for kind in Parser.EXPR:
                if self.show_next().kind == kind:
                    if kind == 'INTEGER_LIT':
                        self.AST.equations[-1].right.list_expr.append(Int(-int(self.show_next().value)))
                    if kind == 'IDENTIFIER':
                        self.AST.equations[-1].right.list_expr.append(Identifier(self.show_next().value, True))
                    self.expect(kind)


        while self.show_next().kind != 'SEMICOLON':
            self.parse_expression(self.AST.equations[-1].right)
        self.expect('SEMICOLON')


    def parse_expression(self, relation):
        if self.show_next().kind == 'LPAREN':
            relation.list_expr.append(Relation()) #ouverture d'une nouvelle relation dans la relation superieure car parentheses
            self.expect('LPAREN')
            if self.show_next().kind == 'MUL' or self.show_next().kind == 'DIV':
                actualToken = self.show_next()
                actualKind = actualToken.kind
                actualPosition = actualToken.position
                print('Error at {}: No expected {} after LPAREN'.format(str(actualPosition), actualKind))
                sys.exit(1)
            while self.show_next().kind != 'RPAREN':
                self.parse_expression(relation.list_expr[-1])
            self.expect('RPAREN')

        expectEXPR = False
        for kind in Parser.OP:
            if self.show_next().kind == kind:
                if relation.list_operateur == None:
                    relation.list_operateur = []
                relation.list_operateur.append(kind)
                self.expect(kind)
                expectEXPR = True

        for kind in Parser.EXPR:
            if self.show_next().kind == kind:
                if kind == 'INTEGER_LIT':
                    relation.list_expr.append(Int(int(self.show_next().value)))
                if kind == 'IDENTIFIER':
                    relation.list_expr.append(Identifier(self.show_next().value))
                self.expect(kind)
                expectEXPR = False
        if expectEXPR :
            actualToken = self.show_next()
            actualPosition = actualToken.position
            print('Error at {}: expected IDENTIFIER or INTEGER_LIT after OP '.format(str(actualPosition)))
            sys.exit(1)

    def check_linear(self):
        for i in range(len(self.AST.equations)):
            equation_i = self.AST.equations[i]
            a = self.cherche(equation_i.left)
            b = self.cherche(equation_i.right)
            if a>=2 or b>=2:
                return(False)
        return(True)

    def cherche(self,relation):
        type_relation = type(Relation())
        type_identifier = type(Identifier("e"))
        if len(relation.list_operateur) == 0:
            return(0)
        for j in range(len(relation.list_operateur)):
            if relation.list_operateur[j] == 'MUL' or relation.list_operateur[j] == 'DIV':
                g = relation.list_expr[j]
                d = relation.list_expr[j+1]
                if type(g) != type_relation and type(d) != type_relation:
                    if type(g) == type_identifier and type(d) == type_identifier:
                        return(2)
                elif type(g) != type_relation:
                    if type(g) == type_identifier:
                        return(1+self.cherche(d))
                    else:
                        return(self.cherche(d))
                elif type(d) != type_relation:
                    if type(d) == type_identifier:
                        return(1+self.cherche(g))
                    else:
                        return(self.cherche(g))
                else:
                    return(self.cherche(g)+self.cherche(d))
            else:
                for x in relation.list_expr:
                    if type(x) == type_identifier:
                        return(1)
                return(0)
