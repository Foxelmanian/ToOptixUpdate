from FEMPy.FEMBody import FEMBody
from FEMPy.CCXPhraser import CCXPhraser, FRDReader, DATReader
from FEMPy.CCXSolver import CCXSolver
from TopologyOptimizer.DensityMaterial import DensityMaterial
from TopologyOptimizer.TopologyOptimizer import TopologyOptimizer
from PolygonMesh.STLPhraser import STL
from PolygonMesh.Geometry import Surface, Solid
import numpy as np
import os


def perform_topology_optimization(voluminaRatio, penal, workDir, solver_path, matSets, maximum_iterations, input_file_path):
    # Import Model
    fem_builder = CCXPhraser(input_file_path)
    fem_body = fem_builder.get_fem_body()

    # Create a material according to the density rule (currently only 1 material is possible no multi material changing)
    topology_optimization_material = DensityMaterial(fem_body.get_materials()[0], 20, 3.0)
    current_density = len(fem_body.get_elements()) * [voluminaRatio]

    # Start with the optimization by changing the material defintion and running optimizer
    ccx_topo_static = CCXSolver(solver_path, input_file_path)
    frd_disp_reader = FRDReader("topo_displacement")
    dat_ener_reader = DATReader("topo_energy")
    optimizer = TopologyOptimizer(current_density, topology_optimization_material)
    sorted_density_element_sets = optimizer.get_element_sets_by_density(fem_body.get_elements())
    output_density = 0.5
    print("Start Optimization")
    for iteration in range(maximum_iterations):
        print("###################################################")
        print("#########")
        print("#------ ITERATION: " + str(iteration + 1) + " of " + str(maximum_iterations) + " ---------")
        print("#########")
        print("###################################################")

        # Define new fem_body


         # Calculate the strain energy density
        ccx_topo_static.run_topo_sys(topology_optimization_material.get_density_materials(), sorted_density_element_sets, "topo_displacement", "U")
        frd_disp_reader.get_displacement(fem_body.get_nodes()) # Mapping displacement to nodes

        ccx_topo_static.run_topo_sens(fem_body.get_nodes(), "topo_energy",fem_body.get_elements(),  "ENER")
        strain_energy_vec = dat_ener_reader.get_energy_density(fem_body.get_elements())
        # Modify material by using the strain energy vector
        optimizer.change_density(strain_energy_vec)

        # Generate STL output of the result and calculate new sorted density set
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
        stl_file.parts.append(topo_part)
        print("Exporting result result elements", len(res_elem))
        if os.path.isfile('STL_res_' + str(iteration) + '.stl'):
            os.remove('STL_res_' + str(iteration) + '.stl')
        stl_file.write(workDir + 'STL_res_' + str(iteration) + '.stl')

        print("###################################################")
        print("#########")
        print("#------ Mean strain energy: " + str(np.mean(strain_energy_vec))  + " ---------")
        print("#########")
        print("###################################################")



if __name__ == "__main__":
    testFile = "example.inp"
    solver_path = "ccx.exe"

    perform_topology_optimization(0.3, 3.0, "test", solver_path, 20, 100, testFile)
