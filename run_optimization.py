## BLENDER from .TopologyOptimizer.OptimizationController import OptimizationController
## PYCHARM from TopologyOptimizer.OptimizationController import OptimizationController
from TopologyOptimizer.OptimizationController import OptimizationController
import os

def run_optimization(penal,  matSets, opti_type, sol_type,
                    weight_factors, max_iteration, vol_frac,
                    files, workDir, solverPath, cpus):
    print('Start topology otpimization')

    os.environ['OMP_NUM_THREADS'] = str(cpus)
    opti_controller = OptimizationController(files, sol_type, reverse=False, type=opti_type)
    opti_controller.set_maximum_iterations(max_iteration)
    opti_controller.set_penalty_exponent(penal)
    opti_controller.set_number_of_material_sets(matSets)
    opti_controller.set_solver_path(solverPath)

    # Start the optimization
    opti_controller.set_result_file_name('stl_result' + str(vol_frac) + "__")
    opti_controller.set_result_path(workDir)
    opti_controller.set_volumina_ratio(vol_frac)
    opti_controller.run()

if __name__ == "__main__":

    # Optimization type --> seperated (combined is not implemented )
    cpus = 4
    opti_type = "seperated"

    # No design space stays until the next definition
    sol_type = ["no_design_space", "static", "no_design_space", "heat"]
    # Use a file with all elements in "no Design space": no_design_space.inp
    files = ["reset_no_design_space.inp", "TwoRectanglesStruc.inp", "reset_no_design_space.inp", "TwoRectanglesTherm.inp"]
    max_iteration = 10
    vol_frac = 0.3
    penal = 3.0
    matSets = 10
    weight_factors = [3.0]
    workDir = "work"
    solverPath = "ccx"
    run_optimization(penal,  matSets, opti_type, sol_type,
                                          weight_factors, max_iteration, vol_frac,
                                          files, workDir, solverPath, cpus)