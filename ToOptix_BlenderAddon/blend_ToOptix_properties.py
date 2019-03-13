import bpy
from bpy.props import *

# global properties for the script, mainly for UI
class TopoOptimizationPropertyGroup(bpy.types.PropertyGroup):


    # FEM - solver path
    solver_path : StringProperty(
        name="solver",
        default='ccx',
        description="Path for CalculiX (or enivornment variable ccx)",
        subtype='FILE_PATH')

    # CPUS
    number_of_cpu : IntProperty(
            name="Number of cpus for FEM Calculation",
            default=3,
            min=1,
            max=6,
            description="Number of cpus which are used for FEM")

    # FEM work path
    work_path : StringProperty(
        name="Result folder",
        description="Path for the results",
        subtype='DIR_PATH')

    # Volumina ratio
    vol_ratio : FloatProperty(
            name="Volumina Ratio",
            default=0.3,
            min=0.0,
            max=1.0,
            precision=2,
            description="Ratio between the design space and solution space")
    # Penalty exponent
    penalty_value : FloatProperty(
            name="Penalty exponent",
            default=3.0,
            min=1.5,
            max = 15.0,
            precision=3,
            description="Exponent for the penalty function by using simp method")
    # Materialsets
    mat_sets : IntProperty(
            name="Material Sets",
            default=20,
            min=2,
            description="Number of sets for the step-material law")
    # Scaling value const
    n_const : IntProperty(
            name="Iterations",
            default=10,
            min=1,
            description="Maximum iterations for calculation")

    # Physic in optimization
    structural_topo : BoolProperty(
            name="Static",
            default=True,
            description="Static load case is selected")

    static_path : StringProperty(
            name="Path",
            description="Which static file path should be selected",
            subtype='FILE_PATH')



    # Physic in optimization
    heat_trans_topo : BoolProperty(
            name="Heat transfer",
            default=True,
            description="Heat transfer load case is selected")

    heat_trans_path : StringProperty(
            name="Path",
            description="Which heat transfer file path should be selected",
            subtype='FILE_PATH')