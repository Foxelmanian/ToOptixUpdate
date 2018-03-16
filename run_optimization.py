from TopologyOptimizer.OptimizationController import OptimizationController
import os


# Set environment variable Windows
cpus = 4
os.popen("set OMP_NUM_THREADS=" + str(cpus))

opti_type = "seperated"
#sol_type = ["heat", "static"]
#files = [ "TwoRectanglesTherm.inp", "TwoRectanglesStruc.inp"]
sol_type = ["heat"]
#"Carrier_no_error_fine_mesh_skeleton.inp", "31_Cube_Finer_mesh.inp", "31_Cube_mittel.inp",
files = [ "31_Cube_grob.inp"]

opti_controller = OptimizationController(files, sol_type, reverse=True, type=opti_type)
opti_controller.run()