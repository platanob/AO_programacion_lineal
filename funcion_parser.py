def parser(problema):
    restricciones = []
     # Expresión regular para extraer las restricciones
    regex_restricciones = r"(-?\d+)x\s*\+?\s*(-?\d+)y\s*(<=|>=|=)\s*(-?\d+)" # busca Coef x e y, operador, valor
    matches = re.finditer(regex_restricciones, problema) 
    for match in matches:
        coeficienteX = int(match.group(1))
        coeficienteY = int(match.group(2))
        operador = match.group(3)
        valor = int(match.group(4))
        restricciones.append({"coeficientes": [coeficienteX, coeficienteY], "operador": operador, "valor": valor})

    # Expresion regular para extraer la funcion objetivo
    regex_objetivo = r"([Mm]inimizar|[Mm]aximizar)\s*Z\s*=\s*(-?\d*\.?\d*)x\s*\+\s*(-?\d*\.?\d*)y"
    match_objetivo = re.search(regex_objetivo, problema) # Buscar coincidencias en la exp regular y el problema
    requerimiento = match_objetivo.group(1)
    coeficienteX = float(match_objetivo.group(2))
    coeficienteY = float(match_objetivo.group(3))
    funcionObjetivo = {"requerimiento": requerimiento, "coeficientes": [coeficienteX, coeficienteY]}
    
    return restricciones, funcionObjetivo




problema = "Minimizar Z = 0.12x + 0.15y\nsujeto a\n60x + 60y >= 300\n12x + 6y >= 36\n10x + 30y >= 90"
restricciones, funcionObjetivo = parser(problema)
p1 = simplexTable(restricciones, funcionObjetivo)