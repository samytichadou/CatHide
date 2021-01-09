import bpy

from ..functions.panel_functions import createPanelCategoriesProperties
from ..addon_prefs import get_addon_preferences
from ..global_variables import cathide_print


def clear_collection(collection) :
    if len(collection)>=1:
        for i in range(len(collection)-1,-1,-1):
            collection.remove(i)


def empty_lists():

    winman = bpy.data.window_managers[0]

    clear_collection(winman.cathide_viewport_panels_categories)


def get_panels_original_categories():

    panel_list = []

    for cat in bpy.data.window_managers[0].cathide_viewport_panels_categories:

        for pan in cat.panels:
            
            panel_list.append([pan.idname, pan.original_category])

    return panel_list


def reset_original_categories(original_cat_list):

    for cat in bpy.data.window_managers[0].cathide_viewport_panels_categories:

        for pan in cat.panels:
            
            for old_panel_entry in original_cat_list:

                if pan.idname == old_panel_entry[0]:
                    
                    pan.original_category = old_panel_entry[1]
                    break


class CATHIDE_OT_refresh_lists(bpy.types.Operator):
    """Refresh CatHide internal Lists"""
    bl_idname = "cathide.refresh_lists"
    bl_label = "Refresh"
    bl_options = {'REGISTER'}


    @classmethod
    def poll(cls, context):
        return True


    def execute(self, context):

        debug = get_addon_preferences().debug

        if debug: print(cathide_print + "Retrieving original categories") #debug

        original_cat_list = get_panels_original_categories()

        if debug: print(cathide_print + "Emptying lists") #debug

        empty_lists()

        if debug: print(cathide_print + "Loading panels : ") #debug

        createPanelCategoriesProperties()

        if debug: print(cathide_print + "Resetting original categories") #debug

        reset_original_categories(original_cat_list)

        return {'FINISHED'}