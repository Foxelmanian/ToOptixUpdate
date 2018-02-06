

class Material(object):

    def __init__(self, name: str):

        self.__name = name
        self.__elasticity = []
        self.__conductivity = []

    def add_elasticity(self, young_module=70000, contraction=0.3, temperature=0.0):
        self.__elasticity.append(Elasticity(young_module, contraction, temperature))

    def add_conductivity(self, conductivity=250, temperature=0.0):
        self.__conductivity.append(Conductivity(conductivity, temperature))

    def __str__(self):
        return ('Name: {} Elasticity entrys: {} Conductivity entrys: {} '.format(
            self.__name, len(self.__elasticity), len(self.__conductivity)))


class Elasticity(object):

    def __init__(self, young_module: float, contraction: float, temperature: float):
        self.__temperature = temperature
        self.__contraction = contraction
        self.__young_module = young_module


class Conductivity(object):

    def __init__(self, conductivity: float, temperature: float):
        self.__temperature = temperature
        self.__conductivity = conductivity
