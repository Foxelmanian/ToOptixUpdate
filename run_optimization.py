from TopologyOptimizer.OptimizationController import OptimizationController
import os

print('Start topology otpimization')
# Set environment variable Windows
cpus = 4
#Windows environment variable
os.popen("set OMP_NUM_THREADS=" + str(cpus))

#Optimization controller settings
opti_type = "seperated"
sol_type = ["static", "heat"]
files = ["TwoRectanglesStruc.inp", "TwoRectanglesTherm"]
opti_controller = OptimizationController(files, sol_type, reverse=True, type=opti_type)
opti_controller.set_maximum_iterations(20)
opti_controller.get_only_last_result()

# Start the optimization
for vol_frac in [0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 0.975]:
    opti_controller.set_result_file_name('stl_result' + str(vol_frac) + "__")
    opti_controller.set_volumina_ratio(vol_frac)
    opti_controller.run()