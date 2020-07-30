import bpy


def getDisplayIcon(prop):
    if prop:
        display_icon = "TRIA_DOWN"
    else:
        display_icon = "TRIA_RIGHT"
    return display_icon


# asset ui list
class CATHIDE_UL_panel_ui_list(bpy.types.UIList): 

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):

        if item.hide:
            layout.enabled = False
        else:
            layout.enabled = True

        if self.layout_type in {'DEFAULT', 'COMPACT'}: 
            layout.label(text = item.name) 
            
        elif self.layout_type in {'GRID'}: 
            layout.alignment = 'CENTER' 
            layout.label(text = item.name)


class CATHIDE_PT_panel(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "View"
    bl_label = "CatHide"

    @classmethod
    def poll(cls, context):
        return True

    def draw(self, context):
        winman = context.window_manager
        viewport_panels_categories = winman.cathide_viewport_panels_categories

        layout = self.layout

        col = layout.column(align=True)

        # categories
        for cat in viewport_panels_categories:
            box = col.box()

            row = box.row(align=True)

            row.prop(cat, 'display', text='', icon=getDisplayIcon(cat.display), emboss=False)

            subrow = row.row()
            if cat.hide:
                subrow.enabled = False
            else:
                subrow.enabled = True
            subrow.label(text=cat.name)

            row.operator('cathide.toggle_category_visibility', text='', icon='HIDE_OFF').cat = cat.name

            # panels
            if cat.display == True:
                viewport_panels_panels = cat.panels

                box.template_list("CATHIDE_UL_panel_ui_list", "", cat, "panels", cat, "panels_index", rows = 3)

                box.prop(cat, "panels_display")

                if cat.panels_display:

                    selected_panel = viewport_panels_panels[cat.panels_index]

                    row = box.row(align=True)
                    row.label(text=selected_panel.idname)
                    row = box.row(align=True)
                    row.label(text=selected_panel.original_category)
                    row = box.row(align=True)
                    row.label(text=selected_panel.context)