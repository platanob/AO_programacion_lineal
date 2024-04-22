import numpy as np
import re

def parser(problema):
    restricciones = []
    regex = r"(-?\d+)x\s*\+?\s*(-?\d+)y\s*(<=|>=|=)\s*(-?\d+)"
    matches = re.finditer(regex, problema)
    for match in matches:
        coeficienteX = int(match.group(1))
        coeficienteY = int(match.group(2))
        operador = match.group(3)
        valor = int(match.group(4))
        restricciones.append({"coeficientes": [coeficienteX, coeficienteY], "operador": operador, "valor": valor})
    return restricciones

class simplexTable:
    def __init__(self, restricciones, funcionObjetivo) -> None:
        self.restricciones = restricciones
        self.coeficientesZ = funcionObjetivo["coeficientes"]
        self.numVariables = len(self.coeficientesZ)
        self.vBasicas = ["Z"]

        self.goe: list = []  # Greater or equal
        self.loe: list = []  # Less or equal
        for restriccion in self.restricciones:
            if restriccion["operador"] == "<=":
                self.loe.append(restriccion)
            elif restriccion["operador"] == ">=":
                self.goe.append(restriccion)

        columnas: int = 2 + self.numVariables + len(self.loe) + len(self.goe)*2
        filas = len(self.restricciones)+1
        self.tabla = np.zeros((filas, columnas))
        self.head = self.makehead()

        if funcionObjetivo["requerimiento"] == "Minimizar":
            z: int = -1
        else:
            z: int = 1

        self.tabla[0][0] = z

        index_a = 1+self.numVariables + \
            len(self.loe) + 1  # indice primera artificial
        i: int = 0
        while i < len(self.goe):  # Inicialización de artificiales
            self.tabla[0][index_a+2*i] = 1
            i += 1

        j: int = 1
        for restriccion in self.goe:
            self.vBasicas.append("a" + str(j))
            for _, coef in enumerate(restriccion["coeficientes"]):
                self.tabla[j][_+1] = coef

            a: int = index_a + (j-1) * 2
            e: int = a-1
            self.tabla[j][e] = -1
            self.tabla[j][a] = 1
            self.tabla[j][len(self.tabla[j])-1] = restriccion["valor"]
            j += 1

        l: int = j
        for index, restriccion in enumerate(self.loe):
            self.vBasicas.append("h" + str(l-j+1))
            for _, coef in enumerate(restriccion["coeficientes"]):
                self.tabla[l][_+1] = coef
            self.tabla[l][index + self.numVariables + 1] = 1
            self.tabla[l][len(self.tabla[l])-1] = restriccion["valor"]
            l += 1

    def makehead(self) -> str:
        head = ["VB", "Z"]

        for i in range(len(self.coeficientesZ)):
            head.append("x" + str(i))

        for i2 in range(len(self.loe)):
            head.append("h" + str(i2))

        for i3 in range(len(self.goe)):
            head.append("e" + str(i3))
            head.append("a" + str(i3))
        head.append("LD")
        return head

    def verTabla(self):
        h1: str = ""

        for h in self.head:
            h1 += h + "\t"
        print(h1)

        j = 0
        for x in self.tabla:
            line: str = self.vBasicas[j] + "\t"
            for y in x:
                line += str(y) + "\t"
            print(line)
            j += 1

problema = "Z = 2x + 2y\nsujeto a\n2x + 1y <= 100\n1x + 3y <= 80\n1x + 0y >= 45\n0x + 1y >= 100"
restricciones = parser(problema)
funcionObjetivo = {"requerimiento": "Minimizar", "coeficientes": [2, 2]}
p1 = simplexTable(restricciones, funcionObjetivo)
p1.verTabla()
