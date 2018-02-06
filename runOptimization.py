from FEMPy.FEMBody import FEMBody
from FEMPy.CCXPhraser import CCXPhraser
from FEMPy.CCXSolver import CCXSolver
from TopologyOptimizer.DensityMaterial import DensityMaterial
from TopologyOptimizer.TopologyOptimizer import TopologyOptimizer
import os
import numpy


def perform_topology_optimization(voluminaRatio, penal, workDir, solver_path, matSets, maximum_iterations, input_file_path):
    # Import Model
    fem_builder = CCXPhraser(input_file_path)
    fem_body = fem_builder.get_fem_body()

    # Create a material according to the density rule (currently only 1 material is possible no multi material changing)
    topology_optimization_material = DensityMaterial(fem_body.get_materials()[0], 20, 3.0).get_density_materials()
    current_density = len(fem_body.get_elements()) * [voluminaRatio]

    # Start with the optimization by changing the material defintion and running optimizer
    ccx_topo_static = CCXSolver(solver_path, input_file_path)

    print("Start Optimization")
    for iteration in range(maximum_iterations):
        print("#------ ITERATION: " + str(iteration + 1) + " of " + str(maximum_iterations) + " ---------")
        # Define new fem_body
        optimizer = TopologyOptimizer(current_density, 20)
        sorted_density_element_sets = optimizer.get_element_sets_by_density(fem_body.get_elements())

        ccx_topo_static.get_topo_opt_displacement(topology_optimization_material, sorted_density_element_sets)




















if __name__ == "__main__":
    testFile = "example.inp"
    solver_path = "ccx.exe"

    perform_topology_optimization(0.3, 3.0, "test", solver_path, 20, 1, testFile)
