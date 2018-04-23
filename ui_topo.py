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

import bpy
from bpy.props import *

import os
import math

import mathutils
from . import run_optimization

__bpydoc__ = """
ToOptix

"""


class OBJECT_OT_start_topo_optimization(bpy.types.Operator):
    """Starts the topology optimization"""
    bl_idname="object.start_topo_optimization"
    bl_label="Run the optimization"
    bl_options = {'REGISTER'}
    bl_category = "TopOptix"
    objName = "lf_topoOpt"

    def execute(self, context):
        scene = context.scene

        # Selecting the variables from GUI
        vol_frac = scene.topoOpt.vol_ratio
        penal = scene.topoOpt.penalty_value
        workDir = scene.topoOpt.work_path
        solverPath = scene.topoOpt.solver_path
        matSets = scene.topoOpt.mat_sets
        max_iteration = scene.topoOpt.n_const

        
        # Finite element system properties
        StructIsActive = scene.topoOpt.structural_topo
        staticPath = scene.topoOpt.static_path

        thermIsActive = scene.topoOpt.heat_trans_topo
        heatPath = scene.topoOpt.heat_trans_path


        cpus = 4
        opti_type = "seperated"
        weight_factors = [1.0, 1.0]
        if StructIsActive:
            sol_type = ["static"]
            files = [staticPath]
            if thermIsActive:
                sol_type = ["static", "heat"]
                files = [staticPath, heatPath]
        elif thermIsActive:
            sol_type = ["heat"]
            files = [heatPath]
        else:
            print("Select a solution type")

        run_optimization.run_optimization(penal,  matSets, opti_type, sol_type,
                                          weight_factors, max_iteration, vol_frac,
                                          files, workDir, solverPath,cpus)

        return {'FINISHED'}


class VIEW3D_OT_topo_opti_tools(bpy.types.Panel):
    '''This class draws the settings for ui'''
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_context = "objectmode"
    bl_category = "ToOptix"
    bl_label = "Topology Optimization ToOptix"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        #-----
        # Checkboxes and values
        #-----

        
        # Solver and working settings
        row = layout.row()
        row.label("Work directory and solver")
        rowsub = layout.row(align=True)
        rowsub.prop(scene.topoOpt, "solver_path")
        rowsub = layout.row(align=True)
        rowsub.prop(scene.topoOpt, "number_of_cpu")
        rowsub = layout.row(align=True)
        rowsub.prop(scene.topoOpt, "work_path")

        
        
        row = layout.row()
        row.label("Optimization iteration and system controll:")
        rowsub = layout.row(align=True)
        rowsub.prop(scene.topoOpt, "n_const")

 
        row = layout.row()
        row.label("Type of physic:")
        rowsub = layout.row(align=True)
        rowsub.prop(scene.topoOpt, "structural_topo")
        rowsub.prop(scene.topoOpt, "static_path")
        rowsub.prop(scene.topoOpt, "weight_static")
        # heat transfer
        rowsub = layout.row(align=True)
        rowsub.prop(scene.topoOpt, "heat_trans_topo")
        rowsub.prop(scene.topoOpt, "heat_trans_path")
        rowsub.prop(scene.topoOpt, "weight_heat_transfer")


        # Settings for material law
        row = layout.row()
        row.label("Settings for material law:")
        rowsub = layout.row(align=True)
        rowsub.prop(scene.topoOpt, "vol_ratio")
        rowsub.prop(scene.topoOpt, "penalty_value")
        rowsub.prop(scene.topoOpt, "mat_sets")

        # create a basemesh
        col = layout.column()
        col.operator("object.start_topo_optimization", "Start optimization")


