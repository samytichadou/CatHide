bl_info = {  
 "name": "CatHide",  
 "author": "Samy Tichadou (tonton)",  
 "version": (1, 0),  
 "blender": (2, 7, 8),  
 "location": "3D View > ToolShelf",  
 "description": "Hide Toolshelf Category from 3D View",  
  "wiki_url": "http://www.samytichadou.com",  
 "tracker_url": "http://www.samytichadou.com/moi",  
 "category": "3D View"}

import bpy
from bpy.props import IntProperty, CollectionProperty , StringProperty , BoolProperty
from bpy.types import Panel
from collections import Counter

# declare UILIST
class CatHideUIList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        
        layout.label(item.name)
        layout.prop(item, "panelstate", text="", emboss=True)

# draw the panel
class CatHidePanel(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Tools"
    bl_label = "Hide Panel"

    def draw(self, context):
        layout = self.layout
        scene=bpy.context.scene
        plist=scene.panel_cathide_list
                
        rows = 7
        row = layout.row()
        row.template_list("CatHideUIList", "", scene, "panel_cathide_list", scene, "cathide_index")
        col = row.column(align=True)
        col.operator("cathide.refresh", text='', icon='FILE_REFRESH')
        col.operator("cathide.apply", text='', icon='FILE_TICK')
                
# refresh cathide collection
class CathideRefresh(bpy.types.Operator):
    bl_idname = "cathide.refresh"
    bl_label = "Refresh"
    bl_description = "Refresh Panel to Hide"
        
    def execute(self, context):
        scene=bpy.context.scene
        plist=scene.panel_cathide_list
        
        #clear panel list
        for i in range(len(plist)-1,-1,-1):
            plist.remove(i)
        
        #declare category list
        catlistreg1=[]
        catlistreg2=[]
        catlistunreg1=[]
        catlistunreg2=[]
        catlistunreg3=[]
        #find category and append them in the list
        for panel in bpy.types.Panel.__subclasses__():
            if hasattr(panel, 'bl_space_type'):
                if hasattr(panel, 'bl_region_type'):
                    if hasattr(panel, 'bl_category'):
                        if panel.bl_space_type=="VIEW_3D":
                            if panel.bl_region_type=="TOOLS":
                                if "bl_rna" not in panel.__dict__:
                                    catlistunreg1.append(panel.bl_category)
                                elif "bl_rna" in panel.__dict__:
                                    catlistreg1.append(panel.bl_category)
                                
        for c1 in list(set(catlistreg1)):
            catlistreg2.append(c1)
            
        for c1 in list(set(catlistunreg1)):
            catlistunreg2.append(c1)
            
        l1=Counter(catlistreg2)
        l2=Counter(catlistunreg2)
        diff=l2-l1
        
        for c in list(diff.elements()):
            catlistunreg3.append(c)
                
        for c2 in catlistreg2:
            newcat=plist.add()
            newcat.name=c2
                
        for c3 in catlistunreg3:
            newcat=plist.add()
            newcat.name=c3
            newcat.panelstate=False
            
        info = 'Panel List refreshed'
        self.report({'INFO'}, info)
        
        return {'FINISHED'}
    
# apply cathide configuration
class CathideApply(bpy.types.Operator):
    bl_idname = "cathide.apply"
    bl_label = "Apply"
    bl_description = "Apply and Hide Panels"
        
    def execute(self, context):
        scene=bpy.context.scene
        plist=scene.panel_cathide_list
        toregister=[]
        tounregister=[]
                
        #register
        for p in plist:
            if p.panelstate==True:
                toregister.append(p.name)
                
        for p in toregister:
            for panel in bpy.types.Panel.__subclasses__():
                if hasattr(panel, 'bl_space_type'):
                    if hasattr(panel, 'bl_region_type'):
                        if hasattr(panel, 'bl_category'):
                            if panel.bl_space_type=="VIEW_3D":
                                if panel.bl_region_type=="TOOLS":
                                    if panel.bl_category==p:
                                        if "bl_rna" not in panel.__dict__:
                                            bpy.utils.register_class(panel)
        #unregister
        for p in plist:
            if p.panelstate==False:
                tounregister.append(p.name)
                
        for p in tounregister:
            for panel in bpy.types.Panel.__subclasses__():
                if hasattr(panel, 'bl_space_type'):
                    if hasattr(panel, 'bl_region_type'):
                        if hasattr(panel, 'bl_category'):
                            if panel.bl_space_type=="VIEW_3D":
                                if panel.bl_region_type=="TOOLS":
                                    if panel.bl_category==p:
                                        if "bl_rna" in panel.__dict__:
                                            bpy.utils.unregister_class(panel)
                                            
        bpy.ops.cathide.refresh()
                                                            
        info = 'Unselected Panels Hidden'
        self.report({'INFO'}, info)
        
        return {'FINISHED'} 

# Create custom property group
class CatHidePanelList(bpy.types.PropertyGroup):
    '''name = StringProperty() '''
    panelstate = bpy.props.BoolProperty(name="panelstate", default = True)
    


# -------------------------------------------------------------------
# register
# -------------------------------------------------------------------

def register():
    bpy.utils.register_class(CatHideUIList)
    bpy.utils.register_class(CatHidePanel)
    bpy.utils.register_class(CathideRefresh)
    bpy.utils.register_class(CathideApply)
    bpy.utils.register_class(CatHidePanelList)
    bpy.types.Scene.panel_cathide_list = \
        bpy.props.CollectionProperty(type=CatHidePanelList)
    bpy.types.Scene.cathide_index = IntProperty()

def unregister():
    bpy.utils.unregister_class(CatHideUIList)
    bpy.utils.unregister_class(CatHidePanel)
    bpy.utils.unregister_class(CathideRefresh)
    bpy.utils.unregister_class(CathideApply)
    bpy.utils.unregister_class(CatHidePanelList)
    del bpy.types.Scene.panel_cathide_list
    del bpy.types.Scene.cathide_index
    
if __name__ == "__main__":
    register()