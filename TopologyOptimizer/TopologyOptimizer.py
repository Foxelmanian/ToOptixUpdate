from typing import List
from FEMPy.Material import Material
from FEMPy.ElementSet import ElementSet

class TopologyOptimizer(object):

    def __init__(self, density: List[float], steps):
        self.__system_answer = []
        self.__system_sensitivity = []
        self.__current_density = density
        self.__steps = steps

    def get_system_answer(self):
        pass

    def get_system_sensitivity(self):
        pass

    def get_element_sets_by_density(self, elements) -> List[ElementSet]:
        element_sets = []
        for i in range(self.__steps):
            element_sets.append([])
        counter = 0
        for key in elements:
            elset_number = (self.__steps - 1) * self.__current_density[counter]
            element_sets[int(elset_number)].append(elements[key])
        element_sets_ob = []
        counter = 1
        for element_id_set in element_sets:

            eset = ElementSet("topoElementSet" + str(counter), element_id_set)
            element_sets_ob.append(eset)
            counter += 1
        return element_sets_ob







