
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

### General information
- Start this program in a user directory so Blender should be for example on the desktop 
- If you want to start Tooptix in "C:Programms\Blender Foundation ..." you need administrator rights (not reccomended)
- So i would suggest you should take a copy of blender and then use it on the desktop or some other user access folder
- (Optional) create a environment variable for Calculix (ccx)

### Blender Installation
- Check if import statement of run_optimization.py is: 
from .TopologyOptimizer.OptimizationController import OptimizationController 
- Copy your ToOptix Folder and paste it into ...\Blender Foundation\Blender\2.79\scripts\addons
- Start Blender and activate the addon (type = mesh)



### Python / PyCharm Installation
- Check if import statement of run_optimization.py is: 
from TopologyOptimizer.OptimizationController import OptimizationController 
- Open the folder with pycharm and just start your optimization


## Settings
- Change file paths in "run_optimization.py"
- Change optimization properties "run_optimization.py"
- Create new cases for CalculiX "test.inp" ....

## Output
- STL File in a specific folder for every optimizaiton step

Example:

```python,example

from run_optimization import run_optimization

cpus = 4
opti_type = "seperated"
sol_type = ["static"]
files = ["testinp\Cylinder_Mesh.inp"]
max_iteration = 20
vol_frac = 0.3
penal = 3.0
matSets = 10
weight_factors = [3.0]
workDir = "work"
solverPath = "ccx"
run_optimization(penal,  matSets, opti_type, sol_type,
                                      weight_factors, max_iteration, vol_frac,
                                      files, workDir, solverPath, cpus)

```


## Licence

GNU GENERAL PUBLIC LICENSE
Version 2, June 1991



