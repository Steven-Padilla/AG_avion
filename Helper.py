from Pasajero import Pasajero
import random

def crear_pasajeros(n_pasajeros):
    pasajeros=[]
    for i in range(n_pasajeros):
        pasajeros.append(Pasajero(i+1,round(random.normalvariate(65,5),1)))

    return pasajeros


