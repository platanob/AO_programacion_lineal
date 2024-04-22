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
            self._dosFases()

    #------------------------------------------------
    # Funciones para armado de tabla
    #------------------------------------------------
    def _tabMayorIgual(self):
        aC= len(self.columnas)  #Indice columna a1
        if "a1" in self.columnas:
            aC = self.columnas.index("a1")

        aF = len(self.variableBasicas) # indice fila a1
        for i,restriccion in enumerate(self.mayorIgual):
            self.variableBasicas.append("a" + str(i+1) )

            for j,coeficiente in enumerate(restriccion["coeficientes"]):
                self.matriz[aF][j+1] = coeficiente
                
            self.matriz[aF][aC + 2*i] = 1
            self.matriz[aF][-1] = restriccion["valor"]
            aF += 1

    def _tabMenorIgual(self):
        aC = len(self.columnas) #indice columna
        aF = len(self.variableBasicas) # indice fila  
        for i,restriccion in enumerate(self.menorIgual):
            nR = aF + i 
            for j,coeficiente in enumerate(restriccion["coeficientes"]) :
                self.matriz[nR][j+1] = coeficiente
            
            self.matriz[nR][ aC +i ]  = 1
            self.variableBasicas.append("h" + str(i+1))
            self.columnas.append("h" + str(i+1))
            self.matriz[nR][-1] = restriccion["valor"]


    def _dosFases(self):
            #-----------------------------------------
            #------------Armado de Tabla--------------
            #-----------------------------------------
            # agregar columnas de variables de decisión 
            for i,coeficiente in enumerate(self.funcionObjetivo["coeficientes"]) :
                self.columnas.append( "x" + str(i+1))

            aC= len(self.columnas) + 1   # indice columna artificial
            count = 0 # numero restriccion
            while count  < len(self.mayorIgual):  
                self.columnas.append("e" + str(count+1))
                self.columnas.append("a" + str(count+1))
                self.matriz[0][aC + 2*count] = 1        # Inicialización de artificiales
                count += 1  

            self._tabMayorIgual()
            self._tabMenorIgual()
            #-------------------------------------------
            #-------------Resolución--------------------
            #-------------------------------------------                
            self.verTabla()
            
    def _normal(self):
        print("normal method")
        #-----------------------------------------
        #------------Armado de Tabla--------------
        #-----------------------------------------
        for i,coeficiente in enumerate(self.funcionObjetivo["coeficientes"]) :
            self.matriz[0][i+1] = coeficiente * -1
            self.columnas.append( "x" + str(i+1))
        self._tabMenorIgual()
        #----------------------------------------
        #------------Resolución------------------
        #----------------------------------------
        while True:
            self.verTabla()
            columna = self._columnaPivote()
            if(columna == 0):
                print("end")
                break
            fila = self._filaPivote(columna)
            self._normalzarFila(fila,columna)
            self._pivotear(fila,columna)

            self.variableBasicas[fila] = self.columnas[columna]
            self.verTabla()

    def _eliminacionGaussiana(self):
        for i,vb in enumerate(self.variableBasicas):
            columna = self.columnas.index(vb)
            for  x in range(self.matriz.shape[0]) :
                if self.matriz[x][columna] != 0 and x != i:
                    self.matriz[x] -= self.matriz[i] 

    def _columnaPivote(self) -> int:
        mini = 0
        columna = 0
        for x in range(1,self.matriz.shape[1]):
            if(self.matriz[0][x] < mini ):
                mini = self.matriz[0][x]
                columna = x

        return columna
                

    def _filaPivote(self,columna) -> int:
        mini = np.Infinity
        fila = 0
        for f in range(1,self.matriz.shape[0]):
            if(self.matriz[f][columna] > 0):
                tmp = self.matriz[f,-1] / self.matriz[f,columna]
                if(tmp < mini):
                    mini = tmp
                    fila = f
        return fila
    
    def _normalzarFila(self,fila,columna):    
        for x in range(self.matriz.shape[1]):
            self.matriz[fila][x] /= self.matriz[fila][columna]

    def _pivotear(self,fila,columna):
        for x in [_ for _ in range(self.matriz.shape[0]) if _ != fila]:
            pivot = self.matriz[x][columna]
            for y in range(self.matriz.shape[1]):
                self.matriz[x][y] =  self.matriz[x][y] - self.matriz[fila][y] * pivot 

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
