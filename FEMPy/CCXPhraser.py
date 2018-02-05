from .FEMBody import FEMBody
from .Node import Node
from .Element import Element
from typing import Dict


class CCXPhraser(object):
    """ Importing a FEM object from a calculix input file

    This FEM object is used for topology optimization
    """

    def __init__(self, file_name: str):

        # Initialize a FEMBody
        try:
            self.__file = open(file_name, "r")
            self.__fem_body = FEMBody(self.__get_nodes(), self.__get_elements())
            self.__file.close()
        except FileNotFoundError as e:
            print(e)

    def get_fem_body(self) -> FEMBody:
        return self.__fem_body

    def __get_nodes(self) -> Dict[int, Node]:
        node_dict = {}
        read_attributes = False
        for line in self.__file:
            if len(line) < 1:
                continue
            if "**" in line:
                continue
            if "*" in line[0]:
                read_attributes = False
            if read_attributes:
                line_items = line[:-1].split(",")
                try:
                    node_id = int(line_items[0])
                    x = float(line_items[1])
                    y = float(line_items[2])
                    z = float(line_items[3])
                    node_dict[node_id] = Node(node_id, x, y, z)
                except IOError as e:
                    print(e)
            if "*NODE" in line.upper():
                read_attributes = True
        return node_dict

    def __get_elements(self) -> Dict[int, Element]:
        element_dict = {}
        read_attributes = False
        for line in self.__file:
            if len(line) < 1:
                continue
            if "**" in line:
                continue
            if "*" in line[0]:
                read_attributes = False
            if read_attributes:
                line_items = line[:-1].split(",")
                try:
                    elem_id = int(line_items[0])
                    node_list = []
                    for node_id in line_items[1: len(line_items) - 1]:
                        node_list.append(int(node_id))
                    element_dict[elem_id] = Element(elem_id, node_list)
                except IOError as e:
                    print(e)
            if "*ELEMENT" in line.upper():
                read_attributes = True
        return element_dict


class CCXModificator(object):

    def __init__(self):
        pass


if __name__ == "__main__":
    n1 = CCXPhraser("example.inp")
