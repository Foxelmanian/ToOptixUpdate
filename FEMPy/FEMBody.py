from .Node import Node
from .Element import Element
from .Material import Material
from typing import Dict


class FEMBody(object):
    """ Body of an FEM object with elements nodes and material data.

    This FEMBody is capable of 1 material settings.
    For different material settings in one body you should create two seperated bodys
    """

    def __init__(self, name: str, nodes: Dict[int, Node], elements:  Dict[int, Element], material: Material):
        self.__nodes = nodes
        self.__elements = elements
        self.__material = material
        self.__name = name

    def get_nodes(self):
        return self.__nodes

    def __str__(self):
        return ('Name: {} Nodes: {} Elements: {} Material: {}'.format(
            self.__name, len(self.__nodes), len(self.__elements), self.__material))




