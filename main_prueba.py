import numpy as np

matriz = []
problema1 = {
    "funcionObjetivo": {"requerimiento": 'Maximizar', "coeficientes": [1.50, 2.75]},
    "restricciones": [
        {"coeficientes": [0.6, 1], "operador": '<=', "valor": 200},
        {"coeficientes": [1,1], "operador": '<=', "valor": 700},  
        {"coeficientes": [1,0], "operador": '>=', "valor": 200},  
         

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
        
        self._solve()

    def _solve(self):
        for restriccion in self.restricciones:
            if(restriccion["operador"] == "<="):
                self.menorIgual.append(restriccion)
            else:
                self.mayorIgual.append(restriccion)

        nFilas = len(self.restricciones) + 1
        nColumnas = (2 + len(self.funcionObjetivo["coeficientes"]) + len(self.menorIgual) 
                    + len(self.mayorIgual) * 2)
        
        self.matriz = np.zeros((nFilas,nColumnas))


        if len(self.mayorIgual) == 0:
            self._normal()
        else:
            self._dosFases()

    #------------------------------------------------
    # Funciones para armado de tabla
    #------------------------------------------------
    def _tabMayorIgual(self):
        aC = len(self.columnas)  # Indice columna a1
        if "a1" in self.columnas:
            aC = self.columnas.index("a1")

        aF = len(self.variableBasicas)  # indice fila a1
        for i, restriccion in enumerate(self.mayorIgual):
            self.variableBasicas.append("a" + str(i+1))

            for j, coeficiente in enumerate(restriccion["coeficientes"]):
                self.matriz[aF][j+1] = coeficiente

            self.matriz[aF][aC + 2*i] = 1
            self.matriz[aF][aC + 2*i -1] = -1

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


            #-------------------------------------------
            #------------- Fase 1 ----------------------
            #------------------------------------------- 
            print("""            #-------------------------------------------
            #------------- Fase 1 ----------------------
            #------------------------------------------- 
""")          
            self.verTabla()
            self._eliminacionGaussiana()
            self.verTabla()
            self._nonegativofuncion()
            #-------------------------------------------
            #------------- Fase 2 ----------------------
            #------------------------------------------- 
            print("""            #-------------------------------------------
            #------------- Fase 2 ----------------------
            #------------------------------------------- 
""")
            self._trablafase2()
            self.verTabla()
            self._eliminacionGaussiana()
            self.verTabla()
            self._nonegativofuncion()


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
            self._pivotear(fila,columna)

            self.variableBasicas[fila] = self.columnas[columna]
            self.verTabla()

    def imp_resultado(self):
        pass

    def _trablafase2(self):
        #ingreso de los valores a la tabla de la funcion objetivo 
        a = 1
        for i  in  self.funcionObjetivo['coeficientes']:
            if self.funcionObjetivo['requerimiento'] == 'Minimizar' :
                self.matriz[0][a] = i
            else :
                self.matriz[0][a] = -i
            a+=1
        #buscar indice de las variables artificiales
        indice_fila_a = [indice for indice, valor in enumerate(self.columnas) if valor.startswith('a')]
        #Eliminar variables aritifciales
        b = 0 
        for columna_a_eliminar in indice_fila_a:
            columna_a_eliminar -= b
            self.matriz = np.hstack((self.matriz[:, :columna_a_eliminar], self.matriz[:, columna_a_eliminar + 1:]))
            b += 1
        self.columnas = [valor for valor in self.columnas if not valor.startswith('a')]
    def _nonegativofuncion(self):
        while min(self.matriz[0][1:len(self.matriz[0])-1])< 0 :
            c_pi = self._columnaPivote()
            f_pi = self._filaPivote(c_pi)
            self._normalzarFila(f_pi,c_pi)
            self._pivotear(f_pi,c_pi)
            self.variableBasicas[f_pi] = self.columnas[c_pi]
            self.verTabla()

    def _eliminacionGaussiana(self):
        for i,vb in enumerate(self.variableBasicas):
            columna = self.columnas.index(vb)
            for  x in range(self.matriz.shape[0]) :
                if self.matriz[x][columna] != 0 and x != i:
                    self.matriz[x] -= self.matriz[i] * self.matriz[x][columna]

    def _columnaPivote(self) -> int:
        mini = 0
        columna = 0
        for x in range(1,self.matriz.shape[1]-1):
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
        guardar_numero = self.matriz[fila][columna]
        for x in range(self.matriz.shape[1]):
            self.matriz[fila][x] /= guardar_numero

    def _pivotear(self,fila,columna):
        for x in [_ for _ in range(self.matriz.shape[0]) if _ != fila]:
            pivot = self.matriz[x][columna]
            for y in range(self.matriz.shape[1]):
                self.matriz[x][y] = round(self.matriz[x][y] - self.matriz[fila][y] * pivot, 10)

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
