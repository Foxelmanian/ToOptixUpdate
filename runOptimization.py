from FEMPy.FEMBody import FEMBody
from FEMPy.CCXPhraser import CCXPhraser
from FEMPy.CCXPhraser import FRDReader
from FEMPy.CCXPhraser import DATReader
from FEMPy.CCXSolver import CCXSolver
from TopologyOptimizer.DensityMaterial import DensityMaterial
from TopologyOptimizer.TopologyOptimizer import TopologyOptimizer
import numpy as np


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

    print("Start Optimization")
    for iteration in range(maximum_iterations):
        print("###################################################")
        print("#########")
        print("#------ ITERATION: " + str(iteration + 1) + " of " + str(maximum_iterations) + " ---------")
        print("#########")
        print("###################################################")
        # Define new fem_body
        sorted_density_element_sets = optimizer.get_element_sets_by_density(fem_body.get_elements())

         # Calculate the strain energy density
        ccx_topo_static.run_topo_sys(topology_optimization_material.get_density_materials(), sorted_density_element_sets, "topo_displacement", "U")
        frd_disp_reader.get_displacement(fem_body.get_nodes()) # Mapping displacement to nodes

        ccx_topo_static.run_topo_sens(fem_body.get_nodes(), "topo_energy",fem_body.get_elements(),  "ENER")
        strain_energy_vec = dat_ener_reader.get_energy_density(fem_body.get_elements())
        # Modify material by using the strain energy vector
        optimizer.change_density(strain_energy_vec)

        print("###################################################")
        print("#########")
        print("#------ Mean strain energy: " + str(np.mean(strain_energy_vec))  + " ---------")
        print("#########")
        print("###################################################")


if __name__ == "__main__":
    testFile = "example.inp"
    solver_path = "ccx.exe"

    perform_topology_optimization(0.3, 3.0, "test", solver_path, 20, 50, testFile)
