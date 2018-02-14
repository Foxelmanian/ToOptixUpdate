from typing import List
from .Node import Node

"""


"""


class Element(object):
    """ This class is used for creating a element of FEM
    """

    def __init__(self, element_id: int, nodes: List[Node]):
        self.__nodes = nodes
        self.__element_id = element_id
        self.__strain_energy = 0.0
        self.__density = 0.0

    def get_id(self) -> int:
        return self.__element_id

    def set_strain_energy(self, strain_energy):
        self.__strain_energy = strain_energy

    def get_strain_energy(self):
        return self.__strain_energy

    def get_nodes(self):
        return self.__nodes

    def get_density(self):
        return self.__density

    def set_density(self, density):
        self.__density = density








