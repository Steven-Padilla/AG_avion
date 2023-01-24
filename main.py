from Helper import crear_pasajeros
import random


class AlgoritmoGenetico:
    def __init__(self, pasajeros, n_individuos):
        # Variables que se pueden modificar
        self.pasajeros = pasajeros
        self.n_individuos = n_individuos
        self.n_generaciones = 10
        self.k = 3
        self.ancho_moto = 150
        self.id_indiv = 1
        # self.cant_genes = arr_numeros(self.n_individuos)
        # self.pasajeros = crear_pasajeros(n_pasajeros)
        self.poblacion = []
        self.nueva_poblacion = []
        self.mejor_individuo = []
        self.peor_individuo = []
        self.primera_gen()

    def primera_gen(self):
        individuo_aux = []
        for pasajero in self.pasajeros:
            individuo_aux.append(pasajero.id)

        for _ in range(self.n_individuos):
            random.shuffle(individuo_aux)
            individuo = individuo_aux.copy()
            aptitud_x = self.calcular_aptitud_x(individuo)
            aptitud_y = self.calcular_aptitud_y(individuo)
            self.poblacion.append(
                {'id': self.id_indiv, 'data': individuo, 'aptitud_x': aptitud_x, 'aptitud_y': aptitud_y})
            self.id_indiv += 1
        print(self.poblacion[0])
        for gen in self.poblacion[0].get('data'):
            print(self.encontrar_pasajero(gen))
        # print(self.poblacion)
        # for individuo in poblacion:
            # print(individuo)
        # for _ in range(self.n_individuos):
        #     random.shuffle(poblacion)
        #     self.crear_individuo(poblacion[:],False)

    def mutacion(self):
        # print("Poblacion iniciales: ", self.poblacion)
        for index, individuo in enumerate(self.nueva_poblacion):
            for _ in range(self.n_mutaciones):
                a, b = random.choices(self.cant_genes, k=2)
                individuo.data[a], individuo.data[b] = individuo.data[b], individuo.data[a]
        # print("Poblacion Mutada: ", self.poblacion)

    def llenar_resultado(self, x):
        # k
        pass

    def generar_rango_cruza(self, x):
        # k
        pass

    def cruza(self, indiv1, indiv2):
        # llenado parametros iniciales
        resultado = []
        indiv1_copy = indiv1.copy()
        index_aux = 0
        resultado = self.llenar_resultado(self.n_individuos)
        a, b = self.generar_rango_cruza(self.cant_genes)

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
        self.crear_individuo(resultado, True)
        print(len(self.poblacion))

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
    def calcular_aptitud_y(self, individuo):
        suma_y = 0
        suma_masa = 0
        y40 = {'y': 40, 'valores': [0, 1, 2, 3]}
        y120 = {'y': 120, 'valores': [4, 5, 6, 7]}
        y200 = {'y': 200, 'valores': [8, 9, 10, 11]}
        y280 = {'y': 280, 'valores': [12, 13, 14, 15]}
        for index, id_pasaj in enumerate(individuo):
            gen_masa=self.encontrar_pasajero(id_pasaj).masa
            if index in y40.get('valores'):
                suma_y += (gen_masa*y40.get('y'))
                suma_masa += gen_masa
            elif index in y120.get('valores'):
                suma_y += (gen_masa*y120.get('y'))
                suma_masa += gen_masa
            elif index in y200.get('valores'):
                suma_y += (gen_masa*y200.get('y'))
                suma_masa += gen_masa
            elif index in y280.get('valores'):
                suma_y += (gen_masa*y280.get('y'))
                suma_masa += gen_masa
        return round(suma_y/suma_masa,1)

    def calcular_aptitud_x(self,individuo):
        x40={'x':40,'valores':[0,4,8,12]}
        x120={'x':120,'valores':[1,5,9,13]}
        x200={'x':200,'valores':[2,6,10,14]}
        x280={'x':280,'valores':[3,7,11,15]}
        
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
    pasajeros=crear_pasajeros(numero_pasajeros) 
    for pasajero in pasajeros:
        print(pasajero)
    AG=AlgoritmoGenetico(pasajeros, numero_pasajeros)
    