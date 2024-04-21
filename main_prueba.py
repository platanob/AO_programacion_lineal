import numpy as np
import re

class simplexTable:
    def __init__(self, funcionObjetivo, restricciones) -> None:
        self.coeficientesZ = funcionObjetivo["coeficientes"]
        self.numVariables = len(self.coeficientesZ)
        self.vBasicas = ["Z"]
        self.restricciones = []

        self.goe: list = []  # Greater or equal
        self.loe: list = []  # Less or equal

        for restriccion in restricciones: 
            self.agregar_restriccion(restriccion)

        columnas: int = 2 + self.numVariables + len(self.loe) + len(self.goe) * 2
        filas = len(self.restricciones) + 1
        self.tabla = np.zeros((filas, columnas))
        self.head = self.makehead()

        if (funcionObjetivo["requerimiento"] == "Minimizar"):
            z: int = -1
        else:
            z: int = 1

        self.tabla[0][0] = z

        index_a = 1+self.numVariables + \
            len(self.loe) + 1  # indice primera artificial
        i: int = 0
        while i < len(self.goe):  # Inicialización de artificiales
            self.tabla[0][index_a + 2 * i] = 1
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
            self.vBasicas.append("h" + str(l - j + 1))
            for _, coef in enumerate(restriccion["coeficientes"]):
                self.tabla[l][_+1] = coef
            self.tabla[l][index + self.numVariables + 1] = 1
            self.tabla[l][len(self.tabla[l])-1] = restriccion["valor"]
            l += 1

    def agregar_restriccion(self, constraint_string):
        # expresión regular para buscar un patron en la cadena de restriccion.
        match = re.match(r'([0-9,]+)\s*(<=|>=)\s*(\d+)', constraint_string)
        if not match:
            raise ValueError("Formato de restricción no válido:", constraint_string)
        
        # Extrae los coeficientes, el operador y el valor de la restricción del objeto de coincidencia.
        coeficientes_str = match.group(1)
        operador = match.group(2)
        valor_str = match.group(3)
        
        coeficientes = [int(x) for x in coeficientes_str.split(",")]
        valor = int(valor_str)
        
        if operador =='<=':
            self.loe.append({"coeficientes": coeficientes, "valor": valor})
        elif operador == '>=':
            self.goe.append({"coeficientes": coeficientes, "valor": valor})

        self.restricciones.append({"coeficientes": coeficientes, "operador": operador, "valor": valor})


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
            line = self.vBasicas[j] + "\t"
            for y in x:
                line += str(y) + "\t"
            print(line)
            j += 1

# Ejemplo de uso
funcionObjetivo = {"requerimiento": 'Minimizar', "coeficientes": [2, 2]}
restricciones = ["2,1 <= 100", "1,3 <= 80", "1,0 >= 45", "0,1 >= 100"]
p1 = simplexTable(funcionObjetivo, restricciones)
p1.verTabla()
