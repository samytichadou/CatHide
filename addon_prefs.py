import bpy
import os

addon_name = os.path.basename(os.path.dirname(__file__))

# addon preferences
class CATHIDE_addon_prefs(bpy.types.AddonPreferences):
    bl_idname = addon_name

    debug : bpy.props.BoolProperty(
        name = "Debug",
        default = False,
        )

    cathide_folder : bpy.props.StringProperty(
        name = "Preferences Folder",
        default = os.path.join(bpy.utils.user_resource('DATAFILES'), "cathide"),
        subtype = "DIR_PATH",
        )

    def draw(self, context):
        layout = self.layout

        layout.prop(self, "debug")
        layout.prop(self, "cathide_folder")


# get addon preferences
def get_addon_preferences():
    addon = bpy.context.preferences.addons.get(addon_name)
    return getattr(addon, "preferences", None)