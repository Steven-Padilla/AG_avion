from Helper import crear_pasajeros, generar_rango_cruza, arr_numeros, llenar_resultado,calcular_data_lista_y,calcular_data_lista_x
import random
import tkinter as tk
from tkinter import messagebox 
import math
import matplotlib.pyplot as plt
import numpy as np
import sys


class AlgoritmoGenetico:
    def __init__(self, pasajeros, n_individuos, n_generaciones, tamanio_asiento, n_filas, separacion_entre_asientos,tamanio_poblacion,n_mutaciones,prob_muta,prob_mutacion_gen):
        # Variables que se pueden modificar
        self.pasajeros = pasajeros
        self.n_individuos = n_individuos
        self.n_generaciones = n_generaciones
        self.tamanio_asiento = tamanio_asiento
        self.n_filas = n_filas
        self.separacion_asientos = separacion_entre_asientos
        self.tamanio_poblacion=tamanio_poblacion
        self.n_mutaciones = n_mutaciones
        self.prob_mutacion=prob_muta
        self.prob_mutacion_gen=prob_mutacion_gen
        self.lista_data_x=calcular_data_lista_x(self.n_filas)
        self.lista_data_y=calcular_data_lista_y(self.n_filas)
        self.id_indiv = 1
        self.cant_genes = arr_numeros(self.n_individuos)
        self.poblacion = []
        self.nueva_poblacion = []
        self.mejor_individuo = []
        self.peor_individuo = []
        self.media_individuo=[]
        self.primera_gen()
        self.bucle_algoritmo()

    def bucle_algoritmo(self):
        aux = 0
        while (aux < self.n_generaciones):
            self.generacion=aux+1
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
            self.graficar_individuos(aux+1)
            self.poda()
            self.mejor_individuo.append(self.poblacion[0])
            self.media_individuo.append(self.poblacion[round(self.tamanio_poblacion/2)])
            self.peor_individuo.append(self.poblacion[self.tamanio_poblacion-1])
            print(f'Mejor individuo: {self.poblacion[0]}')
            print(f'Peor individuo: {self.poblacion[self.tamanio_poblacion-1]}')
            print(f'Generación {aux+1}')
            for indiv in self.poblacion:
                print(indiv)
            aux += 1

    def primera_gen(self):
        individuo_aux = []
        for pasajero in self.pasajeros:
            individuo_aux.append(pasajero.id)

        for _ in range(self.tamanio_poblacion):
            random.shuffle(individuo_aux)
            individuo = individuo_aux.copy()
            self.poblacion.append(self.crear_individuo_con_aptitud(individuo))
        print('Población inicial')
        for individuo in self.poblacion:
            print(individuo)
    def graficar_individuos(self,n_generacion):
        fig,aux=plt.subplots()
        arr_x=[]
        arr_y=[]
        for individuo in self.poblacion:
            arr_x.append(individuo['x'])
            arr_y.append(individuo['y'])
        x=np.array([self.x_centro])
        y=np.array([self.y_centro])
        plt.scatter(x,y,label=f'Centro de masa({self.x_centro},{self.y_centro})',marker='x')
        x=np.array(arr_x)
        y=np.array(arr_y)
        plt.scatter(x,y,label='Individuos',marker='.')
        aux.set_title(f'Individuos en generacion: {n_generacion}',fontdict={'fontsize':20,'fontweight':'bold'})
        aux.set_xlabel('X',fontdict={'fontsize':15,'fontweight':'bold', 'color':'tab:red'})
        aux.set_ylabel('Y',fontdict={'fontsize':15,'fontweight':'bold', 'color':'tab:blue'})
        aux.set_xlim(140,240)
        aux.set_ylim(100,240)
        aux.legend(loc='upper right',prop={'size':10})
        plt.grid()
        plt.savefig(f'./images/generacion_{self.generacion}')
        plt.close()
    def crear_individuo_con_aptitud(self, individuo_data):
        x = self.calcular_x(individuo_data)
        y = self.calcular_y(individuo_data)
        aptitud = round(self.calcular_aptitud(x, y), 2)
        individuo = {'data': individuo_data, 'x':x, 'y':y,
                     'aptitud': aptitud, 'id': self.id_indiv}
        self.id_indiv += 1
        return individuo

    def crear_individuo_sin_coordenadas(self, individuo_data):
        individuo = {'data': individuo_data}
        return individuo

    def agregar_aptitud_a_individuo(self, individuo):
        x = self.calcular_x(individuo['data'])
        y = self.calcular_y(individuo['data'])
        individuo['x']=x
        individuo['y']=y
        individuo['aptitud'] = round(self.calcular_aptitud(x, y), 2)
        individuo['id'] = self.id_indiv
        self.id_indiv += 1

    def calcular_aptitud(self, x, y):
        # (x1=160,y1=160)x2=x,y2=y
        x_centro = ((self.tamanio_asiento*4) +
                    self.separacion_asientos)/2
        y_centro = (80*self.n_filas)/2
        self.x_centro=x_centro
        self.y_centro=y_centro
        return math.sqrt((x-x_centro)**2 + (y-y_centro)**2)

    def mutacion(self, nueva_poblacion):
        # print("Poblacion iniciales: ", self.poblacion)
        for index, individuo in enumerate(nueva_poblacion):
            if random.uniform(0,1) <= self.prob_mutacion:
                for _ in range(self.n_mutaciones):
                    if random.uniform(0,1) <= self.prob_mutacion_gen:
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
        while len(self.poblacion) != self.tamanio_poblacion:
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
        self.wind.geometry("900x400")
        # self.wind.eval("tk::PlaceWindow .")
        self.wind.title('Algoritmo genetico')
        self.wind.columnconfigure(0, weight=0)
        #////
        self.label1=tk.Label(self.wind,text="Ingrese la cantidad de filas del avion:")
        self.label1.grid(column=0, row=0)
        self.filas=tk.IntVar()

        self.entry1=tk.Entry(self.wind, width=20, textvariable=self.filas )
        self.entry1.grid(column=0, row=1)

        self.label7=tk.Label(self.wind,text="Ingrese la media de masa para los pasajeros:")
        self.label7.grid(column=0, row=2)
        self.media=tk.IntVar()

        self.entry7=tk.Entry(self.wind, width=20, textvariable=self.media)
        self.entry7.grid(column=0, row=3)

        self.label8=tk.Label(self.wind,text="Ingrese la desviacion estandar de masa para los pasajeros:")
        self.label8.grid(column=0, row=4)
        self.desviacion_estandar=tk.IntVar()

        self.entry8=tk.Entry(self.wind, width=20, textvariable=self.desviacion_estandar)
        self.entry8.grid(column=0, row=5)

        self.label2=tk.Label(self.wind,text="Ingrese la cantidad de generaciones a crear:")
        self.label2.grid(column=0, row=6)
        self.generaciones=tk.IntVar()

        self.entry2=tk.Entry(self.wind, width=20, textvariable=self.generaciones)
        self.entry2.grid(column=0, row=7)

        self.label2=tk.Label(self.wind,text="Probabilidad de mutación del gen:")
        self.label2.grid(column=0, row=8)
        self.prob_muta_gen=tk.IntVar()

        self.entry2=tk.Entry(self.wind, width=20, textvariable=self.prob_muta_gen)
        self.entry2.grid(column=0, row=9)

        self.label3=tk.Label(self.wind,text="Ingrese la cantidad de pasajeros a abordar :")
        self.label3.grid(column=2, row=0)
        self.pasajeros=tk.IntVar()

        self.entry3=tk.Entry(self.wind, width=20, textvariable=self.pasajeros)
        self.entry3.grid(column=2, row=1)


        self.label4=tk.Label(self.wind,text="Ingrese la cantidad de individuos de la poblacion:")
        self.label4.grid(column=2, row=2)
        self.c_poblacion=tk.IntVar()

        self.entry4=tk.Entry(self.wind, width=20, textvariable=self.c_poblacion)
        self.entry4.grid(column=2, row=3)


        self.label5=tk.Label(self.wind,text="Ingrese la cantidad de veces que se muta el individuo:")
        self.label5.grid(column=2, row=4)
        self.n_mutacion=tk.IntVar()

        self.entry5=tk.Entry(self.wind, width=20, textvariable=self.n_mutacion)
        self.entry5.grid(column=2, row=5)


        self.label6=tk.Label(self.wind,text="Ingrese la probabilidad de mutacion:")
        self.label6.grid(column=2, row=6)
        self.prob_mutacion=tk.IntVar()

        self.entry6=tk.Entry(self.wind, width=20, textvariable=self.prob_mutacion)
        self.entry6.grid(column=2, row=7)

        self.label7=tk.Label(self.wind,text="Ingrese el tamaño del pasillo:")
        self.label7.grid(column=2, row=8)
        self.tamanio_pasillo=tk.IntVar()

        self.entry7=tk.Entry(self.wind, width=20, textvariable=self.tamanio_pasillo)
        self.entry7.grid(column=2, row=9)

        self.boton=tk.Button(self.wind, text="Aplicar", command=self.ingresar_generaciones)
        self.boton.grid(column=1, row=12)
        self.boton.config(command=self.aplicar_datos)

        self.wind.mainloop()
    
    def get_prob_muta_gen(self):
        return self.prob_muta_gen.get()
    def get_tamanio_pasillo(self):
        return self.tamanio_pasillo.get()
    def get_desviacion_estandar(self):
        return self.desviacion_estandar
    def get_media(self):
        return self.media
    def get_prob_mutacion(self):
        prob_mutacion = self.prob_mutacion.get()
        return prob_mutacion
    def get_n_mutacion(self):
        n_mutaciones = self.n_mutacion.get()
        return n_mutaciones
    def get_cantidad_poblacion(self):
        cantidad_poblacion = int(self.c_poblacion.get())
        return cantidad_poblacion
    def ingresar_cantidad_pasajeros_abordar(self):    
        pasajeros=int(self.pasajeros.get())
        return pasajeros
    def ingresar_generaciones(self):
        generaciones = int(self.generaciones.get())
        return generaciones
    def ingresar_fila(self):
        fila = int(self.filas.get())
        return fila
    def aplicar_datos(self):
        if self.pasajeros.get() > (self.filas.get()*4):
            messagebox.showerror("Error", "La cantidad de pasajeros no puede ser mayor al numero de asientos")
            sys.exit(1)
        else:
            self.wind.destroy()
def generar_grafica(algoritmo):
    list_epocas = []
    list_mejores_aptitud = []
    list_peores_aptitud = []
    list_media_aptitud=[]
    for x in algoritmo.media_individuo:
        list_media_aptitud.append(x.get('aptitud'))
    for k in algoritmo.mejor_individuo:
        list_mejores_aptitud.append(k.get('aptitud'))
    for j in algoritmo.peor_individuo:
        list_peores_aptitud.append(j.get('aptitud'))
    for i in range(algoritmo.n_generaciones):
        list_epocas.append(i+1)  
    fig, ax = plt.subplots()
    ax.plot(list_epocas, list_mejores_aptitud,label='Mejores Aptitud')
    ax.plot(list_epocas, list_media_aptitud,label='Aptitud Media')
    ax.plot(list_epocas, list_peores_aptitud, color='red',label='Peores Aptitud')
    ax.legend(loc='upper right')
    plt.show()  

if __name__ == '__main__':
    #Tkinter
    window = tk.Tk()
    entrada= Interfaz(window)
    n_filas = entrada.ingresar_fila()
    numero_pasajeros_max = 4*n_filas
    numero_pasajeros= entrada.ingresar_cantidad_pasajeros_abordar()
    tamanio_poblacion=entrada.get_cantidad_poblacion()
    numero_generaciones = entrada.ingresar_generaciones()
    n_mutaciones=entrada.get_n_mutacion()
    prob_muta=entrada.get_prob_mutacion()
    separacion_asientos = entrada.get_tamanio_pasillo()
    prob_mutacion_gen=entrada.get_prob_muta_gen()
    # Se calcula tomando en cuenta la distancia entre pajeros (asientos)
    tamanio_asiento = 80
    media= entrada.get_media().get()
    desviacion_estandar=entrada.get_desviacion_estandar().get()
    pasajeros = crear_pasajeros(numero_pasajeros,numero_pasajeros_max,media,desviacion_estandar)
    for pasajero in pasajeros:
        print(pasajero)
    print(f'Filas: {n_filas}\nGeneraciones: {numero_generaciones}')
    AG = AlgoritmoGenetico(pasajeros, numero_pasajeros_max, numero_generaciones,
                           tamanio_asiento, n_filas, separacion_asientos,tamanio_poblacion,n_mutaciones,prob_muta,prob_mutacion_gen)
    generar_grafica(AG)
