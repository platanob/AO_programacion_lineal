# Suponiendo que tienes una lista llamada 'lista'
lista = ['Z', 'x1', 'x2', 'e1', 'a1', 'e2', 'a2', 'e3', 'a3']

# Usamos la función filter() para filtrar los elementos que no contienen 'A'
nueva_lista = list(filter(lambda x: 'A' not in x, lista))

print("Lista sin las entradas que contienen 'A':", nueva_lista)
