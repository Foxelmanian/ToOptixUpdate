from .FEMPy.CCXPhraser import CCXPhraser, FRDReader, DATReader
from .FEMPy.CCXSolver import CCXSolver
from TopologyOptimizer.DensityMaterial import DensityMaterial
from TopologyOptimizer.TopologyOptimizer import TopologyOptimizer
from TopologyOptimizer.Filter import ElementFilter
from .FEMPy.Geometry.STLPhraser import STL
from .FEMPy.Geometry.Solid import Solid
from .FEMPy.Geometry.Surface import Surface
import os
import numpy as np


class OptimizationController(object):

    def __init__(self, files, solution_types, reverse=False, type="seperated"):
        self.__reverse = reverse
        self.__type = type
        self.__files = files
        self.__solution_types = solution_types


        self.__volumina_ratio = 0.3
        if self.__reverse:
            self.__volumina_ratio = 1.0 - self.__volumina_ratio

        self.__material_sets = 20
        self.__penalty_exponent = 3
        self.__solver_path = "ccx.exe"
        self.__density_output = 0.5
        self.__result_path = "stl_results"
        self.__maximum_iterations = 100
        self.__run_counter = 0
        self.__change = 0.2
        self.__use_filter = True

    def use_filter(self, boolean_v):
        self.__use_filter = boolean_v

    def set_maximum_iterations(self, maximum_iterations):
        self.__maximum_iterations = maximum_iterations

    def set_maximum_density_change(self, change):
        self.__change = change

    def set_number_of_material_sets(self, number_of_sets):
        self.__material_sets = number_of_sets

    def run(self):
        if not os.path.exists(self.__result_path):
            os.mkdir(self.__result_path)

        if self.__type == "seperated":
            for file, solution_type in zip(self.__files, self.__solution_types):
                if solution_type == "static":
                    # Create each time a new fem body for each type
                    fem_builder = CCXPhraser(file)
                    fem_body = fem_builder.get_fem_body()
                    ele_filter = ElementFilter(fem_body.get_elements())
                    ele_filter.create_filter_structure()

                    self.__optimization(file, fem_body, ele_filter, solution_type)
                    self.__run_counter += 1

                if solution_type == "heat":
                    # Create each time a new fem body for each type
                    fem_builder = CCXPhraser(file)
                    fem_body = fem_builder.get_fem_body()
                    ele_filter = ElementFilter(fem_body.get_elements())
                    ele_filter.create_filter_structure()

                    self.__optimization(file, fem_body, ele_filter, solution_type)
                    self.__run_counter += 1

    def __optimization(self, input_file_path, fem_body, ele_filter, solution_type):

        if solution_type == "heat":
            system_request = "NT"
            sensitivity_request = "HFL"

        elif solution_type == "static":
            system_request = "U"
            sensitivity_request = "ENER"
        else:
            raise ValueError("Solution type not supported")

        sys_file_name = system_request + "_system_optimization"
        sens_file_name = sensitivity_request + "_sensitivity_optimization"
        # Create a material according to the density rule (currently only 1 material is possible no multi material changing)
        topology_optimization_material = DensityMaterial(fem_body.get_materials()[0], self.__material_sets, self.__penalty_exponent)
        current_density = len(fem_body.get_elements()) * [self.__volumina_ratio]
        ccx_topo_static = CCXSolver(self.__solver_path, input_file_path)

        # Calculix Result reader for FRD and DAT
        frd_reader = FRDReader(sys_file_name)
        dat_reader = DATReader(sens_file_name)

        # Build up Optimizater
        optimizer = TopologyOptimizer(current_density, topology_optimization_material)
        optimizer.set_maximum_density_change(self.__change)
        sorted_density_element_sets = optimizer.get_element_sets_by_density(fem_body.get_elements())
        optimizer.set_compaction_ratio(self.__volumina_ratio)

        # Start optimization
        for iteration in range(self.__maximum_iterations):
            #optimizer.set_compaction_ratio(max(self.__volumina_ratio, 1.0 - 0.05 * iteration))
            ccx_topo_static.run_topo_sys(topology_optimization_material.get_density_materials(), sorted_density_element_sets, sys_file_name, system_request)
            if solution_type == "heat":
                frd_reader.get_temperature(fem_body.get_nodes())
            elif solution_type == "static":
                frd_reader.get_displacement(fem_body.get_nodes())
            ccx_topo_static.run_topo_sens(fem_body.get_nodes(), sens_file_name,fem_body.get_elements(),  sensitivity_request)

            if solution_type == "heat":
                sensitivity_vector = dat_reader.get_heat_flux(fem_body.get_elements())
            elif solution_type == "static":
                sensitivity_vector = dat_reader.get_energy_density(fem_body.get_elements())

            # Change densitys
            optimizer.change_density(sensitivity_vector)
            if self.__use_filter:
                print("########## FILTER IS USED")
                optimizer.filter_density(ele_filter)
            sorted_density_element_sets = optimizer.get_element_sets_by_density(fem_body.get_elements())

            # Select results which density is higher than a specific value
            res_elem = []
            for element_key in fem_body.get_elements():
                if self.__reverse:
                    if fem_body.get_elements()[element_key].get_density() < self.__density_output:
                        res_elem.append(fem_body.get_elements()[element_key])
                else:
                    if fem_body.get_elements()[element_key].get_density() > self.__density_output:
                        res_elem.append(fem_body.get_elements()[element_key])

            self.__plot_result(iteration, res_elem)

    def __plot_result(self, iteration, res_elem):
        # Create the Surface for an stl output
        topo_surf = Surface()
        topo_surf.create_surface_on_elements(res_elem)
        print("Number of result elements", len(res_elem))
        stl_file = STL(1)
        topo_part = Solid(1, topo_surf.triangles)
        stl_file.add_solid(topo_part)
        print("Exporting result elements: {}".format(len(res_elem)))
        stl_result_path = os.path.join(self.__result_path, str(self.__run_counter)
                                       + '_STL_res_' + str(iteration) + '.stl')
        print("Exporting stl result: {}".format(stl_result_path))
        if os.path.isfile(stl_result_path):
            os.remove(stl_result_path)
        stl_file.write(stl_result_path)