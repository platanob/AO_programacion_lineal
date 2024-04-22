import numpy as np
matriz = []
problema1 = {
    "funcionObjetivo": {"requerimiento": 'Minimizar', "coeficientes": [2, 2]},
    "restricciones": [
        {"coeficientes": [2, 1], "operador": '<=', "valor": 100},
        {"coeficientes": [1, 3], "operador": '<=', "valor": 80},
        {"coeficientes": [1, 0], "operador": '>=', "valor": 45},
        {"coeficientes": [0, 1], "operador": '>=', "valor": 100},
    ],
}


class simplexTable:
    def __init__(self, problema) -> None:
        self.restricciones = problema["restricciones"]
        self.coeficientesZ = problema["funcionObjetivo"]["coeficientes"]
        self.numVariables = len(self.coeficientesZ)
        self.vBasicas = ["Z"]

        self.goe: list = []  # Greater or equal
        self.loe: list = []  # Less or equal
        for restriccion in self.restricciones:
            if (restriccion["operador"] == "<="):
                self.loe.append(restriccion)
            if (restriccion["operador"] == ">="):
                self.goe.append(restriccion)

        columnas: int = 2 + self.numVariables + len(self.loe) + len(self.goe)*2
        filas = len(self.restricciones)+1
        self.tabla = np.zeros((filas, columnas))
        self.head = self.makehead()

        if (problema["funcionObjetivo"]["requerimiento"] == "Minimizar"):
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


p1 = simplexTable(problema1)
p1.verTabla()
