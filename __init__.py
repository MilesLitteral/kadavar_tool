#====================== BEGIN GPL LICENSE BLOCK ======================
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
#======================= END GPL LICENSE BLOCK ========================

# <pep8 compliant>

bl_info = {
    "name": "Kadavar",
    "version": (1, 0),
    "author": "Miles J. Litteral (Sasori Zero)",
    "blender": (2, 78, 0),
    "description": "Enhanced point merging tools",
    "location": "Alt + K",
    "wiki_url": "N/A",
    "tracker_url": "",
    "warning": "may produce errors, fix in progress",
    "category": "Mesh"}


if "bpy" in locals():
    import importlib

import bpy
import bmesh

class MergeFirstOperator(bpy.types.Operator):
    bl_idname = "wm.merge_first"
    bl_label = "Kadavar_Merge_First"

    def execute(self, context):
        bpy.ops.mesh.merge(type='FIRST', uvs=True)
        return {'FINISHED'}


class MergeLastOperator(bpy.types.Operator):
    bl_idname = "wm.merge_last"
    bl_label = "Kadavar_Merge_Last"

    def execute(self, context):
        bpy.ops.mesh.merge(type='LAST', uvs=True)
        return {'FINISHED'}

class MergeCenterOperator(bpy.types.Operator):
    bl_idname = "wm.merge_center"
    bl_label = "Kadavar_Merge_Center"

    def execute(self, context):
        bpy.ops.mesh.merge(type='CENTER', uvs=True)
        return {'FINISHED'}

class MergePointOperator(bpy.types.Operator):
    bl_idname = "wm.mp_kadavar"
    bl_label = "Kadavar_Merge"

    def execute(self, context):
        XX = []
        vx = []
        dm = bpy.context.object.data

        if bpy.context.object.mode == 'EDIT':
            bm = bmesh.from_edit_mesh(dm)
        elif bpy.context.object.mode == 'OBJECT':
            bm = bmesh.new()
            bm.from_mesh(dm)
            del(XX[:])
            del(vx[:])
            
        for i in bm.select_history:
            vx.append(i)  
            if(len(vx) > 1 and len(vx) < 3):
                XX.append(vx)
            elif(len(vx) <= 1 and len(vx) > 2):
                del(vx[:])

        teng = [(XX[0][0], XX[0][1]), (XX[0][2], XX[0][3])]

        for i in teng:
            bmesh.ops.pointmerge(bm, verts=i, merge_co=i[-1].co)
            bmesh.update_edit_mesh(dm)
            bm.verts.index_update()
            del(XX[:])

        return {'FINISHED'}


class KadavarMenu(bpy.types.Menu):
    bl_idname = "KadavarMenu"
    bl_label = "Kadavar Tool"

    def draw(self, context):
        layout = self.layout

        obj = bpy.context.object
        bm = bmesh.new()
        bm.from_mesh(obj.data)

        layout.operator("wm.mp_kadavar", text="Merge At Point")
        layout.split()
        layout.label(text="Merge Tools")
        layout.split()
        layout.operator("wm.merge_first", text="Merge at first point")
        layout.operator("wm.merge_last",  text="Merge at last point")
        layout.operator("wm.merge_center", text="Merge at Center of points")

# -----------------------------------------------------------------------------
# Functions #
# -----------------------------------------------------------------------------

##### REGISTER #####

def register():
    bpy.utils.register_class(KadavarMenu)
    bpy.utils.register_class(MergePointOperator)
    bpy.utils.register_class(MergeCenterOperator)
    bpy.utils.register_class(MergeLastOperator)
    bpy.utils.register_class(MergeFirstOperator)

    kc = bpy.context.window_manager.keyconfigs.addon

    if kc:
        km = kc.keymaps.new(name="3D View", space_type="VIEW_3D")
        kmi = km.keymap_items.new('wm.call_menu', 'K', 'PRESS', alt=True)
        kmi.properties.name = "KadavarMenu"

def unregister():
    bpy.utils.unregister_class(KadavarMenu)
    bpy.utils.unregister_class(MergePointOperator)
    bpy.utils.unregister_class(MergeCenterOperator)
    bpy.utils.unregister_class(MergeLastOperator)
    bpy.utils.unregister_class(MergeFirstOperator)


    kc = bpy.context.window_manager.keyconfigs.addon
    if kc:
        km = kc.keymaps["3D View"]
        for kmi in km.keymap_items:
            if kmi.idname == 'wm.call_menu':
                if kmi.properties.name == "KadavarMenu":
                    km.keymap_items.remove(kmi)
                    break


if __name__ == "__main__":
    register()

