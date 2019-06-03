import re
import sys
from token import Token

regexExpressions = [
    (r'[ \n\t]+', None),
    (r'#[^\n]*', None),
    (r'Systeme\b', 'SYSTEME'),
    (r'\(', 'LPAREN'),
    (r'\)', 'RPAREN'),
    (r'\{', 'LBRACE'),
    (r'\}', 'RBRACE'),
    (r'\;', 'SEMICOLON'),
    (r'\=', 'ASSIGN'),
    (r'\+', 'ADD'),
    (r'\-', 'SUB'),
    (r'\*', 'MUL'),
    (r'\/', 'DIV'),
    (r'[a-zA-Z]\w*', 'IDENTIFIER'),
    (r'\d+', 'INTEGER_LIT')
]


class Lexer:

    def __init__(self):
        self.tokens = []



    def lex(self, inputText):

        lineNumber = 0
        for line in inputText:
            lineNumber += 1
            position = 0
            while position < len(line):
                match = None
                for tokenRegex in regexExpressions:
                    pattern, tag = tokenRegex
                    regex = re.compile(pattern)
                    match = regex.match(line, position)
                    if match:
                        data = match.group(0)
                        if tag:
                            token = Token(tag, data, [lineNumber, position])
                            self.tokens.append(token)
                            print('TOKEN ', token)
                        break
                if not match:
                    print(inputText[position])
                    print("no match")
                    sys.exit(1)
                else:
                    position = match.end(0)
        print("lexer: analysis successful!")
        return self.tokens

if __name__=="__main__":
    inputText = open("test.txt").readlines()
    lex = Lexer()
    lex.lex(inputText)
