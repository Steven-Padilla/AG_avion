class Pasajero:
    def __init__(self,id,masa):
        self.id=id
        self.masa=masa

    def __repr__(self):
        return str(self.__dict__)