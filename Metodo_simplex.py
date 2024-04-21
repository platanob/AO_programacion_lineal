import re

def parser_expresion(expresion):
    # Utilizamos expresiones regulares para dividir la expresión en componentes
    tokens = re.findall(r'\d+|\+|\-|\*|\/|<=|>=|==|!=|\(|\)', expresion)
    return tokens

expresion = "3 + 4 * (2 - 1) <= 5"
tokens = parser_expresion(expresion)
print("Tokens:", tokens)
