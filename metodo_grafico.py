import re
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon
import math

def parser(problema):
    restricciones = []
    # Expresión regular para extraer las restricciones
    regex_restricciones = r"(-?\d+)x\s*\+?\s*(-?\d+)y\s*(<=|>=|=)\s*(-?\d+)"  # busca Coef x e y, operador, valor

    matches = re.finditer(regex_restricciones, problema)
    for match in matches:
        coeficienteX = int(match.group(1))
        coeficienteY = int(match.group(2))
        operador = match.group(3)
        valor = int(match.group(4))
        restricciones.append({"coeficienteX": coeficienteX, "coeficienteY": coeficienteY, "operador": operador, "valor": valor})

    # Expresion regular para extraer la funcion objetivo
    regex_objetivo = r"([Mm]inimizar|[Mm]aximizar)\s*Z\s*=\s*(-?\d*\.?\d*)x\s*\+\s*(-?\d*\.?\d*)y"
    match_objetivo = re.search(regex_objetivo, problema)  # Buscar coincidencias en la exp regular y el problema
    if match_objetivo:
        requerimiento = match_objetivo.group(1)
        coeficienteX = float(match_objetivo.group(2))
        coeficienteY = float(match_objetivo.group(3))
        funcionObjetivo = {"requerimiento": requerimiento, "coeficienteX":coeficienteX,"coeficienteY":coeficienteY}
    else:
        raise ValueError("No se encontró ninguna coincidencia para la función objetivo")

    return restricciones, funcionObjetivo

def esValido(eq,x,y):
    res = x * eq['coeficienteX'] + y * eq['coeficienteY']

    if eq['operador'] == "<=":
        return res <= eq['valor']
    if eq['operador'] == ">=":
        return res >= eq['valor']
    if eq['operador'] == "=":
        return res == eq['valor']
    

def determinante2x2(matriz):
    return (matriz[0][0] * matriz[1][1]) - (matriz[0][1] * matriz[1][0])

def crammer(eq1, eq2):
    m = [
        [eq1['coeficienteX'], eq1['coeficienteY'], eq1['valor']],
        [eq2['coeficienteX'], eq2['coeficienteY'], eq2['valor']]
    ]

    mx = [
        [eq1['valor'], eq1['coeficienteY']],
        [eq2['valor'], eq2['coeficienteY']],
    ]

    my = [
        [eq1['coeficienteX'], eq1['valor']],
        [eq2['coeficienteX'], eq2['valor']]
    ]

    det = determinante2x2(m)

    if det == 0:
        return {'x': float('NaN'), 'y': float('NaN')}

    detX = determinante2x2(mx)
    detY = determinante2x2(my)

    return {
        'x': detX / det,
        'y': detY / det
    }
    
def validar_puntos(restricciones, x, y):
    response = True
    it = 0

    while it < len(restricciones) and response:
        if not esValido(restricciones[it], x, y):
            response = False
        it += 1

    return response

def evaluar(eq, x, y):

    return x * eq['coeficienteX'] + y * eq['coeficienteY']

def metodo_grafico(pr):
    puntos_facts = []
    puntos_evaluados = []
    intersecciones = []
    
    restricciones, objetivo = parser(pr)
    
    for i in range(len(restricciones)):
        for j in range(i + 1, len(restricciones)):
            p = crammer(restricciones[i], restricciones[j])
            x = p['x']
            y = p['y']
            validated = validar_puntos(restricciones, x, y)
            if validated:
                puntos_facts.append({'x': x, 'y': y})
            intersecciones.append({'x': x, 'y': y})
            
                
    mini = {'x': 0, 'y': 0, 'value': float('inf')}
    maxi = {'x': 0, 'y': 0, 'value': float('-inf')} 
             
    for punto in puntos_facts:
        x, y = punto['x'], punto['y']
        evalue = evaluar(objetivo, x, y)
        if evalue < mini['value']:
            mini = {'x': x, 'y': y, 'value': evalue}
        if evalue > maxi['value']:
            maxi = {'x': x, 'y': y, 'value': evalue}
        puntos_evaluados.append({'x': x, 'y': y, 'value': evalue})
    
    return {
        'funcionObjetivo': objetivo,
        'restricciones': restricciones,
        'maximo': maxi,
        'minimo': mini,
        'puntosRegionFactible': puntos_evaluados,
        'intersecciones': intersecciones
    } 

solucion = metodo_grafico("Minimizar Z = 2x + 2y\nsujeto a\n2x+1y<=100\n1x+3y<=80\n1x+0y<=45\n0x+1y<=100\n1x+0y>=0\n0x+1y>=0")

def calcular_distancia(punto1, punto2):
    x1, y1 = punto1
    x2, y2 = punto2
    distancia = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return distancia

def ordenar_por_cercania(lista_puntos):
    referencia = lista_puntos[0]
    lista_ordenada = sorted(lista_puntos, key=lambda punto: calcular_distancia(referencia, punto))
    return lista_ordenada

def graficar_restricciones(restricciones, intersecciones, funcionObjetivo, puntosRegionFactible):
    
    restricciones2 = restricciones
    restricciones2.append(funcionObjetivo)
    
    for restriccion in restricciones2:
        x = np.linspace(0, 100, 400)
        if restriccion['coeficienteY'] != 0:
            y = (restriccion['valor'] - restriccion['coeficienteX'] * x) / restriccion['coeficienteY']
        else:
            y = x
            x = np.ones(400) * (restriccion['valor'] / restriccion['coeficienteX'])
        plt.plot(x, y, label=f"{restriccion['coeficienteX']}x + {restriccion['coeficienteY']}y {restriccion['operador']} {restriccion['valor']}")
     
    
    # Encontrar la región factible y llenarla
    regionFactible = []
    for p in puntosRegionFactible:
        texto = "\tx:" + str(round(p["x"],2)) + "\ty:" + str(round(p["y"],2)) + "\tz:" + str(round(evaluar(funcionObjetivo,p["x"],p["y"]),2))
        plt.annotate(texto, (p["x"], p["y"]), textcoords="offset points", xytext=(0,10), ha='center', bbox=dict(boxstyle="round,pad=0.3", fc="yellow", ec="black", lw=1))
        regionFactible.append((p['x'],p['y']))
        
    regionFactible = ordenar_por_cercania(regionFactible)
    
    poly = Polygon(regionFactible, closed=True, color='gray', alpha=0.5)
    plt.gca().add_patch(poly)

    # Graficar puntos de intersección
    for interseccion in intersecciones:
        plt.plot(interseccion['x'], interseccion['y'], 'ro')

    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Problema de programación lineal')
    plt.xlim(0, 100)
    plt.ylim(0, 100)
    plt.legend()
    plt.show()

solucion['funcionObjetivo']

if solucion['funcionObjetivo']['requerimiento'] == 'Maximizar':
    solucion['funcionObjetivo']["valor"] = solucion["maximo"]["value"]
else:
    solucion['funcionObjetivo']["valor"] = solucion["minimo"]["value"]
    
solucion['funcionObjetivo']['operador'] = '='

graficar_restricciones(solucion['restricciones'],solucion['intersecciones'],solucion['funcionObjetivo'],solucion['puntosRegionFactible'])