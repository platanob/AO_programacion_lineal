import re


def parser_expresion(expresion):
    # Utilizamos expresiones regulares para dividir la expresión en componentes
    tokens = re.findall(r'\d+|\+|\-|\*|\/|<=|>=|==|!=|\(|\)', expresion)

    return tokens


def leer():
    n_exp = input("Dime el numero de expreciones")
    for i in range(n_exp):
        pass
