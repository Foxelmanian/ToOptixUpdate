from FEMPy.FEMBody import FEMBody
from FEMPy.Node import Node
from FEMPy.Element import Element
from FEMPy.Material import Material
from typing import Dict
from typing import List


class CCXPhraser(object):
    """ Importing a FEM object from a calculix input file

    This FEM object is used for topology optimization
    """

    def __init__(self, file_name: str):

        # Initialize a FEMBody
        try:
            self.__file = open(file_name, "r")
            self.__fem_body = FEMBody("CCXPhraser", self.__get_nodes(), self.__get_elements(), self.__get_material())
            self.__file.close()
        except FileNotFoundError as e:
            print(e)

    def get_fem_body(self) -> FEMBody:
        return self.__fem_body

    def __get_nodes(self) -> Dict[int, Node]:
        node_dict = {}
        read_attributes = False
        self.__file.seek(0)
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
        self.__file.seek(0)
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

    def __get_material(self) -> Material:

        read_elastic = False
        read_conductivity = False
        self.__file.seek(0)
        for line in self.__file:
            if "**" in line:
                continue

            if "*" in line[0]:
                read_elastic = False
                read_conductivity = False

            if read_elastic:
                line_items = line[:-1].split(",")
                try:
                    if len(line_items) <= 2:
                        material.add_elasticity(float(line_items[0]), float(line_items[1]))
                    else:
                        material.add_elasticity(float(line_items[0]), float(line_items[1]), float(line_items[2]))
                except IOError as e:
                    print(e)

            if read_conductivity:
                line_items = line[:-1].split(",")
                try:
                    if len(line_items) <= 2:
                        material.add_conductivity(float(line_items[0]))
                    else:
                        material.add_conductivity(float(line_items[0]), float(line_items[1]))
                except IOError as e:
                    print(e)

            if "*ELASTIC" in line.upper():
                read_elastic = True

            if "*CONDUCTIVITY" in line.upper():
                read_conductivity = True

            if "*MATERIAL" in line.upper():
                tmp_line = line[:-1].split(",")
                name = "unknown"
                for word in tmp_line:
                    if "NAME" in word.upper():
                        name = word.split("=")[1]
                material = Material(name)
        return material

class CCXModificator(object):

    def __init__(self):
        pass

if __name__ == "__main__":
    phraserFEM = CCXPhraser("example.inp")
    fe_body = phraserFEM.get_fem_body()
    print(fe_body)

