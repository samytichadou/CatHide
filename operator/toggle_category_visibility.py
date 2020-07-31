import bpy

from ..functions.panel_functions import getPanelWithId, registerPanel, unregisterPanel


def togglePanelChildsVisibility(panel_property, hide):
    for child in panel_property.child_panels:
        child_id = getPanelWithId(child.idname)

        if hide and not child.hide:
            unregisterPanel(child_id)
            child.hide = True

        elif not hide and child.hide:
            registerPanel(child_id)
            child.hide = False


def toggleCatPanelsVisibility(cat_property, hide):
    for panel in cat_property.panels:
        panel_id = getPanelWithId(panel.idname)

        if hide and not panel.hide:
            unregisterPanel(panel_id)
            panel.hide = True

        elif not hide and panel.hide:
            registerPanel(panel_id)
            panel.hide = False

        if panel.child_panels:
            togglePanelChildsVisibility(panel, hide)


class CATHIDE_OT_toggle_category_visibility(bpy.types.Operator):
    """Go Back to Edit Project"""
    bl_idname = "cathide.toggle_category_visibility"
    bl_label = "Toggle Visibility"
    bl_options = {'REGISTER', 'INTERNAL'}

    cat = bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        winman = context.window_manager

        category = winman.cathide_viewport_panels_categories[self.cat]

        if category.hide:
            category.hide = False
            toggleCatPanelsVisibility(category, False)
        else:
            category.hide = True
            toggleCatPanelsVisibility(category, True)

        return {'FINISHED'}