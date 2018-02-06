
from FEMPy.ElementSet import ElementSet
from typing import List

class CCXSolver(object):

    def __init__(self, solver_path: str, input_deck_path: str):
        self.__solver_path = solver_path
        self.__input_path = input_deck_path

    def get_topo_opt_displacement(self, topo_materials, topo_element_sets):
        tmp_run_file = "disp.inp"
        run_file = open(tmp_run_file, "w")
        run_file.write("*** Topology optimization input deck \n")
        input_deck = open(self.__input_path, "r")

        for line in input_deck:
            if "*STEP" in line.upper():
                for material in topo_materials:
                    run_file.write("*MATERIAL, name=" + str(material.get_name()) + "\n")
                    run_file.write("*ELASTIC \n")
                    for elasticity in material.get_elasticity():
                        run_file.write('{}, {}, {} \n'.format(elasticity.get_young_module(),
                                                           elasticity.get_contraction(),
                                                           elasticity.get_temperature()))
                    run_file.write("*CONDUCTIVITY  \n")
                    for conductivity in material.get_conductivity():
                        run_file.write('{},{}  \n'.format(conductivity.get_conductivity(),
                                                      conductivity.get_temperature()))

                for element_set in topo_element_sets:
                    if len(element_set.get_elements()) <= 0:
                        continue
                    run_file.write("*ELSET,ELSET=" + element_set.get_name() + "\n")
                    tmp_counter = 0
                    for element in element_set.get_elements():
                        tmp_counter += 1
                        if tmp_counter == 8:
                            run_file.write("\n")
                            tmp_counter = 0
                        run_file.write(str(element.get_id()) + ",")
                    run_file.write("\n")

                for ii in range(len(topo_element_sets)):
                    if len(topo_element_sets[ii].get_elements()) <= 0:
                        continue
                    set_name = topo_element_sets[ii].get_name()
                    mat_name = topo_materials[ii].get_name()
                    run_file.write("*SOLID SECTION,ELSET=" + str(set_name) + ",material=" + str(mat_name) + "\n")

            if "*SOLID SECTION" in line.upper():
                continue


            run_file.write(line)
            print(line)
        input_deck.close()
        run_file.close()







