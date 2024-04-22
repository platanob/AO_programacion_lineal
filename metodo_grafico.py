import re
import matplotlib.pyplot as plt
import numpy as np

def is_valid(eq, x, y):
    res = x * eq['coeficienteX'] + y * eq['coeficienteY']

    if eq['operador'] == "<=":
        return res <= eq['valor']
    if eq['operador'] == ">=":
        return res >= eq['valor']
    if eq['operador'] == "=":
        return res == eq['valor']

def get_zeros(eq):
    return {
        'x': eq['valor'] / eq['coeficienteX'],
        'y': eq['valor'] / eq['coeficienteY']
    }

def intersection(eq1, eq2):
    matriz = [[eq1['coeficienteX'], eq1['coeficienteY'], eq1['valor']],
              [eq2['coeficienteX'], eq2['coeficienteY'], eq2['valor']]]

    new_matriz = [[0, 0, 0], [0, 0, 0]]

    for i in range(3):
        new_matriz[0][i] = matriz[0][i] + (matriz[0][1] / matriz[1][1] * -1) * matriz[1][i]
        new_matriz[1][i] = matriz[1][i] + (matriz[1][0] / matriz[0][0] * -1) * matriz[0][i]

    div1 = new_matriz[0][0]
    div2 = new_matriz[1][1]

    for s in range(3):
        new_matriz[0][s] = new_matriz[0][s] / div1
        new_matriz[1][s] = new_matriz[1][s] / div2

    return {'x': new_matriz[0][2], 'y': new_matriz[1][2]}

def parse_problem(problem):
    restricciones = []
    regex = re.compile(r'(-?\d+)x\+?(-?\d+)y(<=|>=|=)(-?\d+)')
    arrCoef = problem.replace(' ', '').split('\n')[2:]

    for inec in arrCoef:
        match = regex.match(inec)
        if match:
            coeficienteX = int(match.group(1))
            coeficienteY = int(match.group(2))
            operador = match.group(3)
            valor = int(match.group(4))
            restricciones.append({'coeficienteX': coeficienteX, 'coeficienteY': coeficienteY, 'operador': operador, 'valor': valor})

    return restricciones

def validate_point(restricciones, x, y):
    it = 0
    while it < len(restricciones):
        if not is_valid(restricciones[it], x, y):
            return False
        it += 1
    return True

def graphic_method(pr):
    puntos_facts = []
    puntos_evaluados = []
    objetivo, restricciones = parse_problem(pr)

    for i in range(len(restricciones)):
        for j in range(i + 1, len(restricciones)):
            x, y = intersection(restricciones[i], restricciones[j])
            if validate_point(restricciones, x, y):
                puntos_facts.append({'x': x, 'y': y})

    mini = {'x': 0, 'y': 0, 'valor': float('inf')}
    maxi = {'x': 0, 'y': 0, 'valor': float('-inf')}
    for punto in puntos_facts:
        if objetivo == 'max':
            evalue = max(punto['x'], punto['y'])
        elif objetivo == 'min':
            evalue = min(punto['x'], punto['y'])
        else:
            raise ValueError("La función objetivo debe ser 'max' o 'min'")
            
        if evalue < mini['value']:
            mini = {'x': punto['x'], 'y': punto['y'], 'value': evalue}
        if evalue > maxi['value']:
            maxi = {'x': punto['x'], 'y': punto['y'], 'value': evalue}

        puntos_evaluados.append({'x': punto['x'], 'y': punto['y'], 'value': evalue})
        
    return {
        'funcionObjetivo': objetivo,
        'restricciones': restricciones,
        'maximo': maxi,
        'minimo': mini,
        'puntosRegionFactible': puntos_evaluados
    }
        
        