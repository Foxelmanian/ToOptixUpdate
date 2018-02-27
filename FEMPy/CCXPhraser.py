from .FEMBody import FEMBody
from .Node import Node
from .Material import Material
from typing import Dict
from .Element import Element

from typing import List


class CCXPhraser(object):
    """ Importing a FEM object from a calculix input file

    This FEM object is used for topology optimization
    """

    def __init__(self, file_name: str):

        # Initialize a FEMBody
        try:
            self.__file = open(file_name, "r")
            self.__nodes = self.__get_nodes()
            self.__elements = self.__get_elements()
            self.__material = self.__get_material()
            self.__fem_body = FEMBody("CCXPhraser", self.__nodes, self.__elements, self.__material)
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
            if "*NODE" in line.upper() \
                    and not "OUTPUT" in line.upper() \
                    and not "PRINT" in line.upper() \
                    and not "FILE" in line.upper():
                read_attributes = True
        return node_dict

    def __get_elements(self) -> Dict[int, Element]:
        element_dict = {}
        read_attributes = False
        self.__file.seek(0)
        nodes_of_one_element = 0
        new_element = True
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
                    # Check if a new element is in this line or adding new nodes by using the node number
                    if new_element:
                        elem_id = int(line_items[0])
                        node_list = []
                        for node_id in line_items[1: len(line_items)]:
                            node_list.append(self.__nodes[int(node_id)])
                        if len(node_list) == nodes_of_one_element:
                            new_element = True
                        else:
                            new_element = False
                            continue
                    if not new_element:
                        for node_id in line_items[0: len(line_items) - 1]:
                            node_list.append(self.__nodes[int(node_id)])

                        if len(node_list) == nodes_of_one_element:
                            new_element = True
                        else:
                            new_element = False
                            continue
                    element_dict[elem_id] = Element(elem_id, node_list)
                except IOError as e:
                    print(e)
            if "*ELEMENT" in line.upper():
                read_attributes = True
                node_number = line.split("C3D")[1][0:2]
                if node_number[1].isdigit():
                    nodes_of_one_element = int(node_number)
                else:
                    nodes_of_one_element = int(node_number[0])
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


class FRDReader(object):

    def __init__(self, file_name: str):
        self.__file_name = file_name + ".frd"

    def get_displacement(self, node_dictonary: Dict[int, Node]):
        frd_file = open(self.__file_name, "r")
        displacement_section = False
        for line in frd_file:
            if len(line) <= 2:
                continue
            if " -4  DISP" in line.upper():
                displacement_section = True

            if displacement_section and " -3" in line:
                displacement_section = False
            if displacement_section and " -1" in line[0:3]:
                node_id = int(line[3:13])
                disp_x = float(line[13:25])
                disp_y = float(line[25:37])
                disp_z = float(line[37:49])
                node_dictonary[node_id].set_displacement(disp_x, disp_y, disp_z)

    def get_temperature(self, node_dictonary: Dict[int, Node]):
        frd_file = open(self.__file_name, "r")
        displacement_section = False
        for line in frd_file:
            if len(line) <= 2:
                continue
            if " -4  NDTEMP" in line.upper():
                displacement_section = True

            if displacement_section and " -3" in line:
                displacement_section = False
            if displacement_section and " -1" in line[0:3]:
                node_id = int(line[3:13])
                temperature = float(line[13:25])
                node_dictonary[node_id].set_temperature(temperature)
"""
    def get_heat_flux(self, element_dictonary: Dict[int, Element]):

        energy_vector = []
        frd_file = open(self.__file_name, "r")
        energy_section = False
        for line in frd_file:
            if len(line) <= 2:
                continue
            if " -4  FLUX" in line.upper():
                energy_section = True

            if energy_section and " -3" in line:
                energy_section = False
            if energy_section and " -1" in line[0:3]:
                print("import", line)
                element_id = int(line[3:13])
                hflx = float(line[13:25])
                hfly = float(line[25:37])
                hflz = float(line[37:49])
                hfl_ges = (hflx**2 + hfly**2 + hflz**2)**0.5
                element_dictonary[element_id].set_heat_flux(hfl_ges)
                energy_vector.append(hfl_ges)
        return energy_vector

    def get_energy_density(self, element_dictonary: Dict[int, Element]):
        energy_vector = []
        frd_file = open(self.__file_name, "r")
        energy_section = False
        for line in frd_file:
            if len(line) <= 2:
                continue
            if " -4  ENER" in line.upper():
                energy_section = True

            if energy_section and " -3" in line:
                energy_section = False
            if energy_section and " -1" in line[0:3]:
                element_id = int(line[3:13])
                strain_energy= float(line[13:25])
                print(element_id)
                element_dictonary[element_id].set_strain_energy(strain_energy)
                energy_vector.append(strain_energy)
        return energy_vector
"""


class DATReader(object):

    def __init__(self, file_name: str):
        self.__file_name = file_name + ".dat"

    def get_energy_density(self, element_dictonary: Dict[int, Element]):

        energy_vector = []
        frd_file = open(self.__file_name, "r")
        energy_section = False
        for line in frd_file:
            if len(line) <= 2:
                continue
            if energy_section:
                element_id = int(line[0:10])
                strain_energy = float(line[15:28])
                element_dictonary[element_id].set_strain_energy(strain_energy)
                energy_vector.append(strain_energy)
            if "INTERNAL ENERGY DENSITY" in line.upper():
                energy_section = True
        return energy_vector

    def get_heat_flux(self, element_dictonary: Dict[int, Element]):

        frd_file = open(self.__file_name, "r")
        energy_section = False
        element_id_before = -1

        for line in frd_file:
            if len(line) <= 2:
                continue
            if energy_section:
                element_id = int(line[0:10])
                hflx_x = float(line[15:28])
                hflx_y = float(line[28:42])
                hflx_z = float(line[42:56])
                ges_hfl = (hflx_x ** 2 + hflx_y ** 2 + hflx_z ** 2) ** 0.5
                if element_id != element_id_before:
                    element_dictonary[element_id].set_heat_flux(ges_hfl)
                    element_id_before = element_id
                else:
                    old_hflx = element_dictonary[element_id].get_heat_flux()
                    element_dictonary[element_id].set_heat_flux(ges_hfl + old_hflx)
            if "HEAT FLUX" in line.upper():
                energy_section = True
        energy_vector = []
        for key in element_dictonary:
            energy_vector.append(element_dictonary[key].get_heat_flux())


        return energy_vector





