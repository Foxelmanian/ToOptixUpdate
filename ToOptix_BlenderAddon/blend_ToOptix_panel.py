import bpy


class ToOptix_PT_Panel(bpy.types.Panel):

    bl_idname = "ToOptix_panel"
    bl_label = "ToOptix"
    bl_category = "ToOptix"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        #-----
        # Checkboxes and values
        #-----
        # Solver and working settings
        row = layout.row()
        row.label(text="Work directory and solver")

        rowsub = layout.row(align=True)
        rowsub.prop(scene.topoOpt, "solver_path")

        
        rowsub = layout.row(align=True)
        rowsub.prop(scene.topoOpt, "number_of_cpu")
        rowsub = layout.row(align=True)
        rowsub.prop(scene.topoOpt, "work_path")

        row = layout.row()
        row.label(text="Optimization iteration and system controll:")
        rowsub = layout.row(align=True)
        rowsub.prop(scene.topoOpt, "n_const")

        row = layout.row()
        row.label(text="Type of physic:")
        rowsub = layout.row(align=True)
        rowsub.prop(scene.topoOpt, "structural_topo")
        rowsub.prop(scene.topoOpt, "static_path")

        # heat transfer
        rowsub = layout.row(align=True)
        rowsub.prop(scene.topoOpt, "heat_trans_topo")
        rowsub.prop(scene.topoOpt, "heat_trans_path")

        # Settings for material law
        row = layout.row()
        row.label(text="Settings for material law:")
        rowsub = layout.row(align=True)
        rowsub.prop(scene.topoOpt, "vol_ratio")
        rowsub.prop(scene.topoOpt, "penalty_value")
        rowsub.prop(scene.topoOpt, "mat_sets")

        # create a basemesh
        col = layout.column()
        col.operator("view3d.run_optimization", text="Start optimization")

