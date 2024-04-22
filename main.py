import numpy as np
import math 
matriz = []
problema1 = {
    "funcionObjetivo": {"requerimiento": 'Minimizar', "coeficientes": [2, 2]},
    "restricciones": [
        {"coeficientes": [2, 1], "operador": '<=', "valor": 100},
        {"coeficientes": [1, 3], "operador": '<=', "valor": 80},
        {"coeficientes": [1, 0], "operador": '<=', "valor": 45},
        {"coeficientes": [0, 1], "operador": '<=', "valor": 100},
    ],
}


class simplexTable:
    def __init__(self, problema) -> None:
        self.matriz = np.array 
        self.restricciones = problema["restricciones"]
        self.funcionObjetivo = problema["funcionObjetivo"]
        self.columnas = ["Z"]
        self.variableBasicas = ["Z"]
        self.mayorIgual = []
        self.menorIgual = []
        
        self._crearTabla()

    def _crearTabla(self):
        for restriccion in self.restricciones:
            if(restriccion["operador"] == "<="):
                self.menorIgual.append(restriccion)
            else:
                self.mayorIgual.append(restriccion)

        nFilas = len(self.restricciones) + 1
        nColumnas = (2 + len(self.funcionObjetivo["coeficientes"]) + len(self.menorIgual) 
                    + len(self.mayorIgual) * 2)
        
        self.matriz = np.zeros((nFilas,nColumnas))

        #---------------------------------------------------------------
        #--------------------------Armar Tabla--------------------------
        #---------------------------------------------------------------


        # Función objetivo
        for i,coeficiente in enumerate(self.funcionObjetivo["coeficientes"]) :
            self.matriz[0][i+1] = coeficiente * -1
            self.columnas.append( "x" + str(i+1))

        # Restricciones 
        for i,restriccion in enumerate(self.menorIgual):
            nR = i+1 # numero restriccion
            for j,coeficiente in enumerate(restriccion["coeficientes"]) :
                self.matriz[nR][j+1] = coeficiente
            
            self.matriz[nR][ len(self.funcionObjetivo["coeficientes"]) + nR]  = 1
            self.variableBasicas.append("h" + str(nR))
            self.columnas.append("h" + str(nR))
            self.matriz[nR][-1] = restriccion["valor"]

        if len(self.mayorIgual) == 0:
            self._normal()
        else:
            self._dosFases()


    def _dosFases(self):
            
            #Inicializar artificiales
            aC= 2+len(self.funcionObjetivo["variables"]) + len(self.loe)   # indice columna artificial
            count = 1 # numero restriccion
            while aC  < self.matriz.shape[0]-1:  
                self.columnas.append("e" + str(count))
                self.columnas.append("a" + str(count))
                self.matriz[0][aC] = 1        # Inicialización de artificiales
                aC += 2
                count += 1  

            #Inicializar restricciones >=
            aF = 1+ len(self.menorIgual) # indice fila artificial
            for i,restriccion in enumerate(self.mayorIgual):
                nR = i+1 # Numero de restriccion
                for j,coeficiente in enumerate(restriccion["coeficientes"]):
                    pass


            
        
    
    def _normal(self):
        #----------------------------------------
        #------------Resolución------------------
        #----------------------------------------

        while True:
            columna = self._columnaPivote()
            if(columna == 0):
                break

            fila = self._filaPivote(columna)
            self._normalzarFila(fila,columna)
            self._pivotear(fila,columna)

            self.variableBasicas[fila] = self.columnas[columna]
            self.verTabla()

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
                tmp = self.matriz[f][-1] / self.matriz[f][columna]
                if(tmp < mini):
                    mini = tmp
                    fila = f
        return fila
    
    def _normalzarFila(self,fila,columna):    
        for x in range(self.matriz.shape[0]):
            self.matriz[fila][x] /= self.matriz[fila][columna]

    def _pivotear(self,fila,columna):
        for x in [_ for _ in range(self.matriz.shape[0]) if _ != fila]:
            pivot = self.matriz[x][columna]
            for y in range(self.matriz.shape[1]):
                self.matriz[x][y] =  self.matriz[x][y] - self.matriz[fila][y] * pivot 

    def verTabla(self):
        head = ""
        for h in self.columnas:
            head += "\t" + h
        print(head)

        for x in range(self.matriz.shape[0]):
            line = self.variableBasicas[x] + "\t"
            for y in range(self.matriz.shape[1]):
                line += str(round(self.matriz[x][y],3)) + "\t"
            print(line)

p1 = simplexTable(problema1)
p1.verTabla()
