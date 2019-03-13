import bpy
from . import run_optimization


class ToOptix_OT_Operator(bpy.types.Operator):

    bl_idname = "view3d.run_optimization"
    bl_label = "ToOptix Operator"
    bl_description = "Start the 3D optimization"

    def execute(self,context):

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
                    files, workDir, solverPath, cpus, no_design_set=None)
        
        return {'FINISHED'}