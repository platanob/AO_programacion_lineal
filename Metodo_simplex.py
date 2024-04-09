import pandas as pd

# Crear la matriz de datos
data = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12]
]

# Crear el DataFrame
df = pd.DataFrame(data,index=[1,2,3],columns=[1,2,3,4])

print(df[3][2])
