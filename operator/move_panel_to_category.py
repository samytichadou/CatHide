import bpy

from ..functions.panel_functions import getPanelWithId, registerPanel, unregisterPanel


def categories_items_callbacks(scene, context):

    cat = context.window_manager.cathide_viewport_panels_categories
    items = []
    for c in cat:
        items.append((c.name, c.name, ""))
    return items


def register_panel_new_category(panel, category):

    unregisterPanel(panel)
    panel.bl_category = category
    registerPanel(panel)


def move_panel_entry_to_new_category_entry(panel_entry, old_category_entry, new_category_entry):

    # add new

    new_panel = new_category_entry.panels.add()

    new_panel.name = panel_entry.name
    new_panel.idname = panel_entry.idname
    new_panel.context = panel_entry.context
    new_panel.original_category = panel_entry.original_category
    new_panel.hide = panel_entry.hide
    new_panel.protected = panel_entry.protected
    
    if panel_entry.child_panels:

        move_panel_childs_entries_to_new_panel_entry(panel_entry, new_panel)

    # remove old

    for i,elm in enumerate(old_category_entry.panels):
        if elm.idname == panel_entry.idname:
            old_category_entry.panels.remove(i)
            break


def move_panel_childs_entries_to_new_panel_entry(old_panel_entry, new_panel_entry):

    for child in old_panel_entry.child_panels:

        new_child = new_panel_entry.child_panels.add()

        new_child.name = child.name
        new_child.idname = child.idname
        new_child.context = child.context
        # new_child.original_category = child.original_category
        new_child.hide = child.hide


class CATHIDE_OT_move_panel_to_category(bpy.types.Operator):
    """Move selected Panel to other Category"""
    bl_idname = "cathide.move_panel_to_category"
    bl_label = "Move Panel to Category"
    bl_options = {'REGISTER', 'INTERNAL'}


    category : bpy.props.StringProperty()

    target_category : bpy.props.EnumProperty(name = "Category", items = categories_items_callbacks)

    cat_entry : None
    panel_entry : None


    @classmethod
    def poll(cls, context):
        return True


    def invoke(self, context, event):

        winman = context.window_manager

        self.cat_entry = winman.cathide_viewport_panels_categories[self.category]
        self.panel_entry = self.cat_entry.panels[self.cat_entry.panels_index]

        return winman.invoke_props_dialog(self)

 
    def draw(self, context):

        layout = self.layout   
        layout.prop(self, 'target_category')


    def execute(self, context):

        winman = context.window_manager

        panel = getPanelWithId(self.panel_entry.idname)

        register_panel_new_category(panel, self.target_category)

        for child in self.panel_entry.child_panels:
            child_panel = getPanelWithId(child.idname)
            register_panel_new_category(child_panel, self.target_category)

        target_category_entry = winman.cathide_viewport_panels_categories[self.target_category]

        move_panel_entry_to_new_category_entry(self.panel_entry, self.cat_entry, target_category_entry)

        return {'FINISHED'}