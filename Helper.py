from Pasajero import Pasajero
import random

def crear_pasajeros(n_pasajeros):
    pasajeros=[]
    for i in range(n_pasajeros):
        pasajeros.append(Pasajero(i+1,round(random.normalvariate(65,5),1)))

    return pasajeros

def generar_rango_cruza(cant_genes):
    # se crea el rango a evaluar en individuo1 y While para que a y b no sean iguales
    a, b = 0, 0
    while a == b:
        a, b = random.choices(cant_genes, k=2)
    # condicion para que "a" siempre sea menor que "b"
    if a > b:
        a, b = b, a
    return a, b

# crea un arreglo temporal con -1 el cual será el arreglo que se retorna como resultado de la cruza
def llenar_resultado(n):
    resultado = []
    for _ in range(n):
        resultado.append(-1)
    return resultado

def arr_numeros(numero):
    arr = []
    for num in range(numero):
        arr.append(num)
    return arr
def calcular_data_lista_x(n_filas):
    list_valores_en_x = [{'x': 40, 'valores': []}, {'x': 120, 'valores': []}, {
            'x': 250, 'valores': []}, {'x': 330, 'valores': []}]
    aux_fila = 0
    for _ in range(n_filas):
        for i in range(4):
            list_valores_en_x[i]['valores'].append(aux_fila)
            aux_fila += 1
    return list_valores_en_x
def calcular_data_lista_y(n_filas):
    list_valores_en_y=[]
    aux_fila = 0
    valor_en_y = 40
    for _ in range(n_filas):
        list_valores_en_y.append(
            {'y': valor_en_y, 'valores': [aux_fila, aux_fila+1, aux_fila+2, aux_fila+3]})
        aux_fila += 4
        valor_en_y += 80
    return list_valores_en_y