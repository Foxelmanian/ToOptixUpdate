from TopologyOptimizer.OptimizationController import OptimizationController
import os
# Set environment variable Windows
cpus = 4
#Windows environment variable
os.popen("set OMP_NUM_THREADS=" + str(cpus))

#Optimization controller settings
opti_type = "seperated"
sol_type = ["heat", "static"]
files = ["TwoRectanglesTherm.inp", "TwoRectanglesStruc.inp"]
opti_controller = OptimizationController(files, sol_type, reverse=True, type=opti_type)

# Start the optimization
opti_controller.run()