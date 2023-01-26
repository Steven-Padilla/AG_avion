from Helper import crear_pasajeros, generar_rango_cruza, arr_numeros, llenar_resultado,calcular_data_lista_y,calcular_data_lista_x
import random
import tkinter as tk
import math
import matplotlib.pyplot as plt


class AlgoritmoGenetico:
    def __init__(self, pasajeros, n_individuos, n_generaciones, distancia_entre_asientos, n_filas, separacion_entre_asientos):
        # Variables que se pueden modificar
        self.pasajeros = pasajeros
        self.n_individuos = n_individuos
        self.n_generaciones = n_generaciones
        self.distancia_entre_asientos = distancia_entre_asientos
        self.n_filas = n_filas
        self.separacion_asientos = separacion_entre_asientos
        self.n_mutaciones = 2
        self.k = 3
        self.lista_data_x=calcular_data_lista_x(self.n_filas)
        self.lista_data_y=calcular_data_lista_y(self.n_filas)
        self.id_indiv = 1
        self.cant_genes = arr_numeros(self.n_individuos)
        self.poblacion = []
        self.nueva_poblacion = []
        self.mejor_individuo = []
        self.peor_individuo = []
        self.primera_gen()
        self.bucle_algoritmo()

    def bucle_algoritmo(self):
        aux = 0
        while (aux < self.n_generaciones):
            poblacion_nueva = []
            # Hacer todo el bucle del algoritmo
            for i in range(len(self.poblacion)):
                if i == (len(self.poblacion)-1):
                    individuo = self.cruza(self.poblacion[i].get(
                        'data'), self.poblacion[0].get('data'))
                    poblacion_nueva.append(individuo)
                else:
                    individuo = self.cruza(self.poblacion[i].get(
                        'data'), self.poblacion[i+1].get('data'))
                    poblacion_nueva.append(individuo)
            # Se hace la mutación
            self.mutacion(poblacion_nueva)

            # Se calcula la aptitud para cada individuo y se agrega id
            for indiv in poblacion_nueva:
                self.agregar_aptitud_a_individuo(indiv)

            # Se insertan los nuevos en la población general
            for indiv in poblacion_nueva:
                self.poblacion.append(indiv)
            self.ordenar_poblacion_por_aptitud()
            # Poda hasta tener el numero de individuos iniciales
            self.poda()
            self.mejor_individuo.append(self.poblacion[0])
            self.peor_individuo.append(self.poblacion[self.n_filas-1])
            print(f'Mejor individuo: {self.poblacion[0]}')
            print(f'Peor individuo: {self.poblacion[self.n_individuos-1]}')
            print(f'Generación {aux+1}')
            for indiv in self.poblacion:
                print(indiv)
            aux += 1

    def primera_gen(self):
        individuo_aux = []
        for pasajero in self.pasajeros:
            individuo_aux.append(pasajero.id)

        for _ in range(self.n_individuos):
            random.shuffle(individuo_aux)
            individuo = individuo_aux.copy()
            self.poblacion.append(self.crear_individuo_con_aptitud(individuo))
        print('Población inicial')
        for individuo in self.poblacion:
            print(individuo)

    def crear_individuo_con_aptitud(self, individuo_data):
        x = self.calcular_x(individuo_data)
        y = self.calcular_y(individuo_data)
        aptitud = round(self.calcular_aptitud(x, y), 2)
        individuo = {'data': individuo_data,
                     'aptitud': aptitud, 'id': self.id_indiv}
        self.id_indiv += 1
        return individuo

    def crear_individuo_sin_coordenadas(self, individuo_data):
        individuo = {'data': individuo_data}
        return individuo

    def agregar_aptitud_a_individuo(self, individuo):
        x = self.calcular_x(individuo['data'])
        y = self.calcular_y(individuo['data'])
        individuo['aptitud'] = round(self.calcular_aptitud(x, y), 2)
        individuo['id'] = self.id_indiv
        self.id_indiv += 1

    def calcular_aptitud(self, x, y):
        # (x1=160,y1=160)x2=x,y2=y
        x_centro = ((self.distancia_entre_asientos*4) +
                    self.separacion_asientos)/2
        y_centro = (80*self.n_filas)/2
        return math.sqrt((x-x_centro)**2 + (y-y_centro)**2)

    def mutacion(self, nueva_poblacion):
        # print("Poblacion iniciales: ", self.poblacion)
        for index, individuo in enumerate(nueva_poblacion):
            for _ in range(self.n_mutaciones):
                a, b = random.choices(self.cant_genes, k=2)
                individuo.get('data')[a], individuo.get('data')[
                    b] = individuo.get('data')[b], individuo.get('data')[a]
        # print("Poblacion Mutada: ", self.poblacion)

    def cruza(self, indiv1, indiv2):
        # llenado parametros iniciales
        resultado = []
        indiv1_copy = indiv1.copy()
        index_aux = 0
        # Se crea un arreglo temporal con -1 el cual será el arreglo que se retorna como resultado de la cruza
        resultado = llenar_resultado(self.n_individuos)
        a, b = generar_rango_cruza(self.cant_genes)

        # se introduce a resultado los valores seleccionados del primer individuo
        for i in range(a, b+1):
            resultado[i] = indiv1[i]
            index_aux = i

        # for para eliminar los datos que ya se usaron del individuo1 (se creó un arreglo auxiliar)
        for i in range(a, b+1):
            indiv1_copy.remove(indiv1[i])

        datos_restantes = len(indiv1)-len(indiv1[a:b+1])
        index_aux += 1
        aux_result = index_aux
        aux_indv2 = index_aux
        for _ in range(datos_restantes):

            band = False
            while band == False:
                if aux_indv2 >= len(indiv2):
                    aux_indv2 = 0
                if aux_result >= len(resultado):
                    aux_result = 0
                if indiv2[aux_indv2] in indiv1_copy:
                    resultado[aux_result] = indiv2[aux_indv2]
                    indiv1_copy.remove(indiv2[aux_indv2])
                    aux_result += 1
                    aux_indv2 += 1
                    band = True
                else:
                    aux_indv2 += 1

        individuo = self.crear_individuo_sin_coordenadas(resultado)
        return individuo

    def ordenar_poblacion_por_aptitud(self):
        self.poblacion.sort(key=lambda aptitud: aptitud['aptitud'])

    def poda(self):
        while len(self.poblacion) != self.n_individuos:
            self.poblacion.pop()

    def encontrar_pasajero(self, target_id):
        for pasajero in self.pasajeros:
            if pasajero.id == target_id:
                return pasajero

    def calcular_y(self, individuo):
        suma_y = 0
        suma_masa = 0
        list_valores_en_y = self.lista_data_y.copy()
        for index, id_pasaj in enumerate(individuo):
            gen_masa = self.encontrar_pasajero(id_pasaj).masa
            for valores in list_valores_en_y:
                if index in valores['valores']:
                    suma_y += (valores['y']*gen_masa)
                    suma_masa += gen_masa

        return round(suma_y/suma_masa, 1)

    def calcular_x(self, individuo):
        suma_x = 0
        suma_masa = 0
        list_valores_en_x = self.lista_data_x.copy()
        for index, id_pasaj in enumerate(individuo):
            gen_masa = self.encontrar_pasajero(id_pasaj).masa
            for valores in list_valores_en_x:
                if index in valores['valores']:
                    suma_x += (valores['x']*gen_masa)
                    suma_masa += gen_masa
        return round(suma_x/suma_masa, 1)

class Interfaz:
    def __init__(self, window):
        #TKinter
        self.wind = window
        self.wind.geometry("600x250")
        self.wind.eval("tk::PlaceWindow . center")
        self.wind.title('Algoritmo genetico')
        self.wind.columnconfigure(0, weight=1)
        #////
        self.label1=tk.Label(self.wind,text="Ingrese la cantidad de filas del avion:")
        self.label1.grid(column=0, row=0)
        self.filas=tk.IntVar()

        self.entry1=tk.Entry(self.wind, width=10, textvariable=self.filas)
        self.entry1.grid(column=0, row=1)

        self.label2=tk.Label(self.wind,text="Ingrese la cantidad de generaciones a crear:")
        self.label2.grid(column=0, row=2)
        self.generaciones=tk.IntVar()

        self.entry2=tk.Entry(self.wind, width=10, textvariable=self.generaciones)
        self.entry2.grid(column=0, row=3)

        self.boton=tk.Button(self.wind, text="Aplicar", command=self.ingresar_generaciones)
        self.boton.grid(column=0, row=4)
        self.boton.config(command=self.ingresar_fila)
        self.boton.config(command=self.aplicar_datos)

        self.wind.mainloop()
    
    def ingresar_generaciones(self):
        generaciones = int(self.generaciones.get())
        return generaciones
    def ingresar_fila(self):
        fila = int(self.filas.get())
        return fila
    def aplicar_datos(self):
        self.wind.quit()
def generar_grafica(algoritmo):
    list_epocas = []
    list_mejores_aptitud = []
    list_peores_aptitud = []
    for k in algoritmo.mejor_individuo:
        list_mejores_aptitud.append(k.get('aptitud'))
    for j in algoritmo.peor_individuo:
        list_peores_aptitud.append(j.get('aptitud'))
    for i in range(algoritmo.n_generaciones):
        list_epocas.append(i+1)  
    fig, ax = plt.subplots()
    ax.plot(list_epocas, list_mejores_aptitud,label='Mejores Aptitud')
    ax.plot(list_epocas, list_peores_aptitud, color='red',label='Peores Aptitud')
    ax.legend(loc='upper right')
    plt.show()  

if __name__ == '__main__':
    #Tkinter
    window = tk.Tk()
    entrada= Interfaz(window)
    n_filas = entrada.ingresar_fila()
    numero_pasajeros = 4*n_filas
    numero_generaciones=5
    numero_generaciones = entrada.ingresar_generaciones()
    separacion_asientos = 50
    # Se calcula tomando en cuenta la distancia entre pajeros (asientos)
    tamaño_asiento = 80
    pasajeros = crear_pasajeros(numero_pasajeros)
    print(f'Filas: {n_filas}\nGeneraciones: {numero_generaciones}')
    AG = AlgoritmoGenetico(pasajeros, numero_pasajeros, numero_generaciones,
                           tamaño_asiento, n_filas, separacion_asientos)
    generar_grafica(AG)
