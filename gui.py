import bpy

from .global_variables import exception_panels


def get_display_icon(prop):
    if prop:
        display_icon = "TRIA_DOWN"
    else:
        display_icon = "TRIA_RIGHT"
    return display_icon


# asset ui list
class CATHIDE_UL_panel_ui_list(bpy.types.UIList): 

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):

        if item.hide or item.idname in exception_panels:
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

            row.prop(cat, 'display', text='', icon=get_display_icon(cat.display), emboss=False)

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

                try:
                    selected_panel = viewport_panels_panels[cat.panels_index]
                except IndexError:
                    selected_panel = None

                if selected_panel:

                    row = box.row(align=True)
                    row.operator('cathide.move_panel_to_category', text = "Move").category = cat.name

                    row = box.row(align=True)
                    row.prop(cat, "panels_display", text='', icon=get_display_icon(cat.panels_display), emboss=False)
                    row.label(text="Details")

                    if cat.panels_display:

                        col = box.column(align=True)

                        row = col.row(align=True)
                        row.label(text=selected_panel.idname)
                        row = col.row(align=True)
                        row.label(text = "Originally : ")
                        row.label(text=selected_panel.original_category)

                        if selected_panel.context:
                            context_text = selected_panel.context
                        else:
                            context_text = "No context"

                        row = col.row(align=True)
                        row.label(text=context_text)