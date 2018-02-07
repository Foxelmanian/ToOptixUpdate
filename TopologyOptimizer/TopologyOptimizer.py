from typing import List
from FEMPy.Material import Material
from FEMPy.ElementSet import ElementSet
import numpy as np

class TopologyOptimizer(object):

    def __init__(self, density: List[float], steps):
        self.__system_answer = []
        self.__system_sensitivity = []
        self.__current_density = np.array(density)
        self.__next_density = np.array(density)
        self.__steps = steps
        self.__exponent = 3.0
        self.__convergence_max = 0.01
        self.__max_change = 0.2
        self.__compaction_ratio = 0.3

    def get_current_density(self):
        return self.__current_density

    def get_element_sets_by_density(self, elements) -> List[ElementSet]:
        element_sets = []
        for i in range(self.__steps):
            element_sets.append([])
        counter = 0
        for key in elements:
            elset_number = (self.__steps - 1) * self.__current_density[counter]
            counter += 1
            element_sets[int(elset_number)].append(elements[key])
        element_sets_ob = []
        counter = 1
        for element_id_set in element_sets:
            eset = ElementSet("topoElementSet" + str(counter), element_id_set)
            element_sets_ob.append(eset)
            counter += 1
        return element_sets_ob

    def change_density(self, sensitivity):
        sensitivity = np.array(self.__current_density)**(self.__exponent-1) * np.array(sensitivity)
        if min(sensitivity) <= 0:
            sensitivity += abs(min(sensitivity) + 0.1)
        l_upper = max(sensitivity)
        l_lower = min(sensitivity)

        while(abs(l_upper - l_lower) > (l_upper * self.__convergence_max)):
            l_mid = 0.5 * (l_lower + l_upper)
            # Values between 0 and 1
            # SIMP method
            self.__next_density = np.maximum(0.0,
                                             np.maximum(self.__current_density - self.__max_change,
                                                        np.minimum(1.0,
                                                                   np.minimum(self.__current_density + self.__max_change,
                                                                   self.__current_density * (sensitivity / l_mid) ** 0.5))))
            # BESO-Method
            #new_design_variable = np.maximum(0.00001, np.sign(sensitivity - l_mid))

            if np.mean(self.__next_density) - self.__compaction_ratio > 0.0:
                l_lower = l_mid
            else:
                l_upper = l_mid
        print("##---- MEAN DENSTIY: " + str(np.mean(self.__next_density)))
        self.__current_density = self.__next_density









