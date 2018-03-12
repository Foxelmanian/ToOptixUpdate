from TopologyOptimizer.OptimizationController import OptimizationController
import os


# Set environment variable Windows
cpus = 4
os.popen("set OMP_NUM_THREADS=" + str(cpus))

opti_type = "seperated"
sol_type = ["heat", "static"]
files = [ "TwoRectanglesTherm.inp", "TwoRectanglesStruc.inp"]
opti_controller = OptimizationController(files, sol_type, opti_type)
opti_controller.run()