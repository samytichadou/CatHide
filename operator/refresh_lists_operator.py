import bpy

from ..functions.panel_functions import createPanelCategoriesProperties
from ..functions.list_functions import empty_lists, get_panels_original_categories


class CATHIDE_OT_refresh_lists(bpy.types.Operator):
    """Refresh CatHide internal Lists"""
    bl_idname = "cathide.refresh_lists"
    bl_label = "Refresh"
    bl_options = {'REGISTER'}


    refresh_original_categories : bpy.props.BoolProperty(default=False)

    @classmethod
    def poll(cls, context):
        return True


    def execute(self, context):

        print("CatHide retrieving original categories") #debug

        get_panels_original_categories()

        print("CatHide emptying lists") #debug

        empty_lists()

        print("CatHide loading panels : ") #debug

        createPanelCategoriesProperties()

        return {'FINISHED'}