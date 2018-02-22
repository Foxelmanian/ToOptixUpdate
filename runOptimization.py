from FEMPy.FEMBody import FEMBody
from FEMPy.CCXPhraser import CCXPhraser, FRDReader, DATReader
from FEMPy.CCXSolver import CCXSolver
from TopologyOptimizer.DensityMaterial import DensityMaterial
from TopologyOptimizer.TopologyOptimizer import TopologyOptimizer
from TopologyOptimizer.Filter import ElementFilter
from PolygonMesh.STLPhraser import STL
from PolygonMesh.Geometry import Surface, Solid
import numpy as np
import os


def perform_topology_optimization(volumina_ratio, penalty_exponent, work_path, solver_path, matSets, maximum_iterations, input_file_path, input_file_path2):
    # Import Model
    fem_builder = CCXPhraser(input_file_path)
    fem_body = fem_builder.get_fem_body()

    # Create a material according to the density rule (currently only 1 material is possible no multi material changing)
    topology_optimization_material = DensityMaterial(fem_body.get_materials()[0], 20, penalty_exponent)
    current_density = len(fem_body.get_elements()) * [volumina_ratio]

    # Start with the optimization by changing the material defintion and running optimizer
    ccx_topo_static = CCXSolver(solver_path, input_file_path)
    ccx_topo_heat = CCXSolver(solver_path, input_file_path2)

    frd_disp_reader = FRDReader("topo_displacement")
    frd_temp_reader = FRDReader("topo_temperature")
    dat_ener_reader = DATReader("topo_energy")
    frd_hfl_reader = FRDReader("topo_heatflux")
    optimizer = TopologyOptimizer(current_density, topology_optimization_material)
    sorted_density_element_sets = optimizer.get_element_sets_by_density(fem_body.get_elements())
    output_density = 0.5
    print("Start Optimization")

    if not os.path.exists(work_path):
        os.mkdir(work_path)
    # Create Filter by using the element structure
    ele_filter = ElementFilter(fem_body.get_elements())
    ele_filter.create_filter_structure()


    for iteration in range(maximum_iterations):
        print("###################################################")
        print("#########")
        print("#------ ITERATION: " + str(iteration + 1) + " of " + str(maximum_iterations) + " ---------")
        print("#########")
        print("###################################################")
        optimizer.set_compaction_ratio(max(volumina_ratio, 1.0 - 0.05 * iteration))

        # -------------------------- STATIC Topology Optimization --------------------------
        """
        ccx_topo_static.run_topo_sys(topology_optimization_material.get_density_materials(), sorted_density_element_sets, "topo_displacement", "U")
        frd_disp_reader.get_displacement(fem_body.get_nodes())
        # Sensitivity
        ccx_topo_static.run_topo_sens(fem_body.get_nodes(), "topo_energy",fem_body.get_elements(),  "ENER")

        strain_energy_vec = dat_ener_reader.get_energy_density(fem_body.get_elements())
        ############filtered_strain_energy = ele_filter.filter_sensitivity(strain_energy_vec)
        optimizer.change_density(strain_energy_vec)
        sorted_density_element_sets = optimizer.get_element_sets_by_density(fem_body.get_elements())
        """


        # -------------------------- Heat Topology Optimization ----------------------------------
        ccx_topo_heat.run_topo_sys(topology_optimization_material.get_density_materials(), sorted_density_element_sets, "topo_temperature", "NT")
        frd_temp_reader.get_temperature(fem_body.get_nodes())
        ccx_topo_heat.run_topo_sens(fem_body.get_nodes(), "topo_heatflux", fem_body.get_elements(), "HFL")
        heat_flux_vec = frd_hfl_reader.get_heat_flux(fem_body.get_elements())



        print(heat_flux_vec)
        #######filtered_strain_energy = ele_filter.filter_sensitivity(heat_flux_vec)
        optimizer.change_density(heat_flux_vec)
        sorted_density_element_sets = optimizer.get_element_sets_by_density(fem_body.get_elements())












        res_elem = []
        for element_key in fem_body.get_elements():
            if fem_body.get_elements()[element_key].get_density() > output_density:
                res_elem.append(fem_body.get_elements()[element_key])

        print("Export Results")
        topo_surf = Surface()
        topo_surf.create_surface_on_elements(res_elem)
        print("Number of result elements", len(res_elem))
        stl_file = STL(1)
        topo_part = Solid(1, topo_surf.triangles)
        stl_file.add_solid(topo_part)
        print("Exporting result elements: {}".format(len(res_elem)))
        stl_result_path = os.path.join(work_path, 'STL_res_' + str(iteration) + '.stl')
        print("Exporting stl result: {}".format(stl_result_path))
        if os.path.isfile(stl_result_path):
            os.remove(stl_result_path)
        stl_file.write(stl_result_path)

        print("###################################################")
        print("#########")
        print("#------ Mean strain energy: " + str(np.mean(strain_energy_vec))  + " ---------")
        print("#########")
        print("###################################################")


if __name__ == "__main__":
    testFile = "TwoRectanglesStruc.inp"
    testFile2 = "TwoRectanglesTherm.inp"
    solver_path = "ccx.exe"
    work_path = "stlResults"
    perform_topology_optimization(0.3, 3.0, "stlResults", solver_path, 20, 100, testFile, testFile2)
