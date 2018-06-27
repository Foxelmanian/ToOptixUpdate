# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

'''The following program uses any fem-program with an
inputdeck for topology optimisation

There are several classes which are needed for the initializing of
the nodes and elements. If you want to add a fem-program which does
not exist, just implement an ascci-file. And change the output ascci.
The whole optimisation process works with several dictonarys in
which are nodes and elements are saved.

Source code:
             Name: Denk, Martin
             Date: 02.2016
             Accronym: DMST
'''



bl_info = {
    "name": "Topologie Optimization",
    "author": "Martin Denk",
    "description": "Topology optimization for different type of physics",
    "version": (0, 3, 0),
    "blender": (2, 64, 0),
    "location": "View3D > Tool Shelf > ToOptix",
    "url": "None",
    "wiki_url": "None",
    "category": "Mesh"
}


if "bpy" in locals():
    import importlib
    importlib.reload(ui_topo)
else:
    from . import ui_topo


import bpy
from bpy.props import *


# global properties for the script, mainly for UI
class TopoOptimizationPropertyGroup(bpy.types.PropertyGroup):


    # FEM - solver path
    solver_path = StringProperty(
        name="solver",
        description="Path for CalculiX (or enivornment variable ccx)",
        subtype='FILE_PATH')

    # CPUS
    number_of_cpu = IntProperty(
            name="Number of cpus for FEM Calculation",
            default=3,
            min=1,
            max=6,
            description="Number of cpus which are used for FEM")

    # FEM work path
    work_path = StringProperty(
        name="Result folder",
        description="Path for the results",
        subtype='DIR_PATH')

    # Volumina ratio
    vol_ratio = FloatProperty(
            name="Volumina Ratio",
            default=0.3,
            min=0.0,
            max=1.0,
            precision=2,
            description="Ratio between the design space and solution space")
    # Penalty exponent
    penalty_value = FloatProperty(
            name="Penalty exponent",
            default=3.0,
            min=1.5,
            max = 15.0,
            precision=3,
            description="Exponent for the penalty function by using simp method")
    # Materialsets
    mat_sets = IntProperty(
            name="Material Sets",
            default=20,
            min=2,
            description="Number of sets for the step-material law")
    # Scaling value const
    n_const = IntProperty(
            name="Iterations",
            default=10,
            min=1,
            description="Maximum iterations for calculation")

    # Physic in optimization
    structural_topo = BoolProperty(
            name="Static",
            default=True,
            description="Static load case is selected")

    static_path = StringProperty(
            name="Path",
            description="Which static file path should be selected",
            subtype='FILE_PATH')



    # Physic in optimization
    heat_trans_topo = BoolProperty(
            name="Heat transfer",
            default=True,
            description="Heat transfer load case is selected")

    heat_trans_path = StringProperty(
            name="Path",
            description="Which heat transfer file path should be selected",
            subtype='FILE_PATH')




def register():
    # register properties
    bpy.utils.register_class(TopoOptimizationPropertyGroup)
    bpy.types.Scene.topoOpt = bpy.props.PointerProperty(type=TopoOptimizationPropertyGroup)
    bpy.utils.register_module(__name__)


def unregister():
    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()
