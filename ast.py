from visitor import Visitor

class Ast:
    def __init__(self, name):
        self.name = name

    def accept(self, visitor, arg):
        nom = self.__class__.__name__
        print("debug : ",visitor,arg)
        nomMethode = getattr(visitor, "visit" + nom)
        nomMethode(self, arg)

class Systeme(Ast):
    def __init__(self):
        self.equations = []
    def __str__(self):
        return '----------SYSTEME----------'

class Equation(Ast):
    def __init__(self):
        self.left = None #contient des objets Relation
        self.right = None

    def __str__(self):
        string =''
        string = string + ' {} '.format(self.left)
        string = string + ' = '
        string = string + ' {} '.format(self.right)
        return string
    def __repr__(self):
        string =''
        string = string + ' {} '.format(self.left)
        string = string + ' = '
        string = string + ' {} '.format(self.right)
        return string

class Relation(Ast):
    def __init__(self):
        self.list_expr = [] #Element : relation ou expression
        #expression = soit Identifier soit Int
        self.list_operateur = []#None # + - * /

    def __str__(self):
        string = "{} \n{} ".format(self.list_expr, self.list_operateur)
        return string

    def __repr__(self):
        if self.list_operateur == None:
            string = "{} \n".format(self.list_expr)
        else :
            string = "{} \n{} ".format(self.list_expr, self.list_operateur)
        return string

class Int(Ast):
    def __init__(self, val):
            self.value = val

    def __str__(self):
        return "{}".format(self.value)
    def __repr__(self):
        return "{}".format(self.value)

class Identifier(Ast): #class pour les variables
    def __init__(self, string,sg = False):
        self.ident = string
        self.signe = sg # False : pas de signe; True = un signe moins

    def __str__(self):
        if self.signe:
            string = "-{}".format(self.ident)
        else:
            string = "{}".format(self.ident)
        return string

    def __repr__(self):
        if self.signe:
            string = "-{}".format(self.ident)
        else:
            string = "{}".format(self.ident)
        return string
