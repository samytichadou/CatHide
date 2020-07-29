import bpy


def getDisplayIcon(prop):
    if prop:
        display_icon = "TRIA_DOWN"
    else:
        display_icon = "TRIA_RIGHT"
    return display_icon


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
            row.label(text=cat.name)
            row.operator('cathide.toggle_category_visibility', text='', icon='HIDE_OFF').cat = cat.name

            # panels
            if cat.display == True:
                viewport_panels_panels = cat.panels
                col = box.column(align=True)

                for panel in viewport_panels_panels:
                    subbox = col.box()
                    row = subbox.row(align=True)
                    row.prop(panel, 'display', text='', icon=getDisplayIcon(panel.display), emboss=False)
                    row.label(text=panel.name)

                    # panel info
                    if panel.display:
                        row = subbox.row(align=True)
                        row.label(text=panel.idname)
                        row = subbox.row(align=True)
                        row.label(text=panel.context)
                        row = subbox.row(align=True)
                        row.label(text=panel.original_category)

                        if panel.child_panels:
                            row = subbox.row(align=True)
                            row.prop(panel, 'child_display', text='', icon=getDisplayIcon(panel.child_display), emboss=False)
                            row.label(text="Child Panels")