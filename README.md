
# Topology optimization with ToOptix

<p align="center">
  <img src="https://github.com/DMST1990/ToOptixUpdate/blob/master/Images/StaticLoadCaseTwoRectangle.png" width="100%">
</p>


<p align="center">
  <img src="https://github.com/DMST1990/ToOptixUpdate/blob/master/Images/HeatLoadCaseTwoRectangle.png" width="100%">
</p>


## Current version
- Only 3D-FEM support
- Heat Transfer
- Static load case
- Material will change only in young module and conductivity
- Filter selects only the element around the filter object

## Installation
- Install python 3.xx
- Download ToOptix
- Start "runOptimization.py"


## Settings
- Change file paths in "runOptimization.py"
- Change optimization properties "runOptimization.py"
- Create new cases for CalculiX "test.inp" ....

## Output
- STL File in a specific folder for every optimizaiton step

Example:

```python,example

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

```


## Licence

GNU GENERAL PUBLIC LICENSE
Version 2, June 1991



