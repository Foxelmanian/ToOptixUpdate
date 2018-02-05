from .Node import Node
from .Element import Element
from typing import Dict


class FEMBody(object):

    def __init__(self, nodes: Dict[int, Node], elements:  Dict[int, Element]):

        self.__nodes = nodes
        self.__elements = elements

    def get_nodes(self):
        return self.__nodes




