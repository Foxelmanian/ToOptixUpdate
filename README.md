

# Topology optimization with ToOptix


<p align="center">
  <img src="https://github.com/DMST1990/ToOptixUpdate/blob/master/Images/StaticLoadCaseTwoRectangle.png" width="20%">
</p>


<p align="center">
  <img src="https://github.com/DMST1990/ToOptixUpdate/blob/master/Images/HeatLoadCaseTwoRectangle.png" width="20%">
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
- STL File

Example:

```python,test

testFile = "TwoRectanglesStruc.inp"
testFile2 = "TwoRectanglesTherm.inp"
solver_path = "ccx.exe"
work_path = "stlResults"
perform_topology_optimization(0.3, 3.0, "stlResults", solver_path, 20, 100, testFile, testFile2)


```


## Licence

GNU GENERAL PUBLIC LICENSE
Version 2, June 1991




