# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "ToOptix",
    "author" : "Martin Denk",
    "description" : "Wrapper for ToOptix a Topology optimization tool",
    "blender" : (2, 80, 0),
    "location" : "View3D",
    "warning" : "",
    "category" : "Mesh"
}

import bpy

from .blend_ToOptix_run import ToOptix_OT_Operator
from .blend_ToOptix_panel import ToOptix_PT_Panel
from .blend_ToOptix_properties import TopoOptimizationPropertyGroup


def register():
    bpy.utils.register_class(TopoOptimizationPropertyGroup)
    bpy.types.Scene.topoOpt = bpy.props.PointerProperty(type=TopoOptimizationPropertyGroup)

    bpy.utils.register_class(ToOptix_OT_Operator)
    bpy.utils.register_class(ToOptix_PT_Panel)

def unregister():
    bpy.utils.unregister_class(TopoOptimizationPropertyGroup)
    bpy.utils.unregister_class(ToOptix_OT_Operator)
    bpy.utils.unregister_class(ToOptix_PT_Panel)

if __name__ == "__main__":
    register()
