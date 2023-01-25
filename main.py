from Helper import crear_pasajeros,generar_rango_cruza,arr_numeros,llenar_resultado
import random
import math


class AlgoritmoGenetico:
    def __init__(self, pasajeros, n_individuos,n_generaciones,distancia_entre_asientos,n_filas,separacion_entre_asientos):
        # Variables que se pueden modificar
        self.pasajeros = pasajeros
        self.n_individuos = n_individuos
        self.n_generaciones = n_generaciones
        self.distancia_entre_asientos=distancia_entre_asientos
        self.n_filas=n_filas
        self.separacion_asientos=separacion_entre_asientos
        self.n_mutaciones=2
        self.k = 3
        self.ancho_moto = 150
        self.id_indiv = 1
        self.cant_genes = arr_numeros(self.n_individuos)
        self.poblacion = []
        self.nueva_poblacion = []
        self.mejor_individuo = []
        self.peor_individuo = []
        self.primera_gen()
        self.bucle_algoritmo()

    def bucle_algoritmo(self):
        aux=0
        while(aux<self.n_generaciones):
            poblacion_nueva=[]
            #Hacer todo el bucle del algoritmo
            for i in range(len(self.poblacion)):                
                if i==(len(self.poblacion)-1):
                    individuo=self.cruza(self.poblacion[i].get('data'), self.poblacion[0].get('data'))
                    poblacion_nueva.append(individuo)
                else:    
                    individuo=self.cruza(self.poblacion[i].get('data'), self.poblacion[i+1].get('data'))
                    poblacion_nueva.append(individuo)
            #Se hace la mutación
            self.mutacion(poblacion_nueva)
            
            #Se calcula la aptitud para cada individuo y se agrega id
            for indiv in poblacion_nueva:
                self.agregar_aptitud_a_individuo(indiv)
            
            #Se insertan los nuevos en la población general
            for indiv in poblacion_nueva:
                self.poblacion.append(indiv)
            self.ordenar_poblacion_por_aptitud()
            print("Poblacion antes de la poda")
            for indiv in self.poblacion:
                print(indiv)


            #Acá va la poda
            
            aux+=1

    def primera_gen(self):
        individuo_aux = []
        for pasajero in self.pasajeros:
            individuo_aux.append(pasajero.id)

        for _ in range(self.n_individuos):
            random.shuffle(individuo_aux)
            individuo = individuo_aux.copy()
            self.poblacion.append(self.crear_individuo_con_aptitud(individuo))
        print ('Población inicial')
        for individuo in self.poblacion:
            print(individuo)
    
    def crear_individuo_con_aptitud(self, individuo_data):
        x=self.calcular_x(individuo_data)
        y=self.calcular_y(individuo_data)
        aptitud=round(self.calcular_aptitud(x,y),2)
        individuo={'data': individuo_data,'aptitud':aptitud,'id': self.id_indiv}
        self.id_indiv += 1
        return individuo

    def crear_individuo_sin_coordenadas(self, individuo_data):
        individuo={'data': individuo_data}
        return individuo
    def agregar_aptitud_a_individuo(self, individuo):
        x = self.calcular_x(individuo['data'])
        y = self.calcular_y(individuo['data'])
        individuo['aptitud']=round(self.calcular_aptitud(x,y),2)
        individuo['id'] = self.id_indiv
        self.id_indiv += 1
    def calcular_aptitud(self,x,y):
        #(x1=160,y1=160)x2=x,y2=y
        x_centro=((self.distancia_entre_asientos*4)+self.separacion_asientos)/2
        y_centro=(80*self.n_filas)/2
        return math.sqrt((x-x_centro)**2 + (y-y_centro)**2)

    def mutacion(self,nueva_poblacion):
        # print("Poblacion iniciales: ", self.poblacion)
        for index, individuo in enumerate(nueva_poblacion):
            for _ in range(self.n_mutaciones):
                a, b = random.choices(self.cant_genes, k=2)
                individuo.get('data')[a], individuo.get('data')[b] = individuo.get('data')[b], individuo.get('data')[a]
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
        
        individuo=self.crear_individuo_sin_coordenadas(resultado)
        return individuo
    def ordenar_poblacion_por_aptitud(self):
        self.poblacion.sort(key=lambda aptitud: aptitud['aptitud'])

    def poda(self):
        self.ordenar_poblacion()
        for indiv in self.poblacion:
            print(indiv)
        while len(self.poblacion) != self.n_individuos:
            self.poblacion.pop()
        poblacion_copy = self.poblacion.copy()
        self.mejor_individuo.append(poblacion_copy[0].ganancia)
        self.peor_individuo.append(
            poblacion_copy[self.n_individuos-1].ganancia)

    def encontrar_pasajero(self, target_id):
        for pasajero in self.pasajeros:
            if pasajero.id == target_id:
                return pasajero

    # [0 ,1 ,2 ,3 ,
    # 4 ,5 ,6 ,7 ,
    # 8 ,9 ,10,11,
    # 12,13,14,15]
    def calcular_y(self, individuo):
        suma_y = 0
        suma_masa = 0
        list_valores_en_y = []
        aux_fila=0
        valor_en_y=40
        for _ in range(self.n_filas):
            list_valores_en_y.append({'y':valor_en_y,'valores':[aux_fila,aux_fila+1,aux_fila+2,aux_fila+3]})
            aux_fila+=4
            valor_en_y+=80
        # y40 = {'y': 40, 'valores': [0, 1, 2, 3]}
        # y120 = {'y': 120, 'valores': [4, 5, 6, 7]}
        # y200 = {'y': 200, 'valores': [8, 9, 10, 11]}
        # y280 = {'y': 280, 'valores': [12, 13, 14, 15]}
        for index, id_pasaj in enumerate(individuo):
            gen_masa=self.encontrar_pasajero(id_pasaj).masa
            for valores in list_valores_en_y:
                if index in valores['valores']:
                    suma_y += (valores['y']*gen_masa)
                    suma_masa += gen_masa
        # for index, id_pasaj in enumerate(individuo):
        #     gen_masa=self.encontrar_pasajero(id_pasaj).masa
        #     if index in y40.get('valores'):
        #         suma_y += (gen_masa*y40.get('y'))
        #         suma_masa += gen_masa
        #     elif index in y120.get('valores'):
        #         suma_y += (gen_masa*y120.get('y'))
        #         suma_masa += gen_masa
        #     elif index in y200.get('valores'):
        #         suma_y += (gen_masa*y200.get('y'))
        #         suma_masa += gen_masa
        #     elif index in y280.get('valores'):
        #         suma_y += (gen_masa*y280.get('y'))
        #         suma_masa += gen_masa
        return round(suma_y/suma_masa,1)

    def calcular_x(self,individuo):
        x40={'x':40,'valores':[0,4,8,12]}
        x120={'x':120,'valores':[1,5,9,13]}
        x200={'x':200+self.separacion_asientos,'valores':[2,6,10,14]}
        x280={'x':280+self.separacion_asientos,'valores':[3,7,11,15]}
        
        suma_x=0
        suma_masa=0
        for index,id_pasaj in enumerate(individuo):
            gen_masa=self.encontrar_pasajero(id_pasaj).masa
            if index in x40.get('valores'):
                suma_x+=(gen_masa*x40.get('x'))
                suma_masa+=gen_masa
            elif index in x120.get('valores'):
                suma_x+=(gen_masa*x120.get('x'))
                suma_masa+=gen_masa
            elif index in x200.get('valores'):
                suma_x+=(gen_masa*x200.get('x'))
                suma_masa+=gen_masa
            elif index in x280.get('valores'):
                suma_x+=(gen_masa*x280.get('x'))
                suma_masa+=gen_masa
        return round(suma_x/suma_masa,1)
            
if __name__ == '__main__':
    n_filas=4 #Valor constante definido en la planeación de la resolución
    numero_pasajeros=4*n_filas
    numero_generaciones=1
    separacion_asientos=50
    #Se calcula tomando en cuenta la distancia entre pajeros (asientos)
    tamaño_asiento=80
    pasajeros=crear_pasajeros(numero_pasajeros) 
    AG=AlgoritmoGenetico(pasajeros, numero_pasajeros,numero_generaciones,tamaño_asiento,n_filas,separacion_asientos)
    