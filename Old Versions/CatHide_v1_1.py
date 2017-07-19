bl_info = {  
 "name": "CatHide",  
 "author": "Samy Tichadou (tonton)",  
 "version": (1, 1),  
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
        
class CatHidePresetUIList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        layout.prop(item, "name", text="", icon='SETTINGS',  emboss=False, translate=False)
        
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
        prlist=scene.preset_cathide_list
        idx=scene.cathide_preset_index
        activelist=[]
        unactivelist=[]
        
        if len(prlist)>=1 and (idx+1) <= len(prlist):
            tmp1=prlist[idx].activepanel.split(",,")
            tmp2=prlist[idx].unactivepanel.split(",,")
            for p in tmp1:
                activelist.append(p)
            for p in tmp2:
                unactivelist.append(p)
        
        row = layout.row()
        row.label("Panels", icon='MENU_PANEL')
        rows = 7
        row = layout.row()
        row.template_list("CatHideUIList", "", scene, "panel_cathide_list", scene, "cathide_index")
        col = row.column(align=True)
        col.operator("cathide.refresh", text='', icon='FILE_REFRESH')
        col.operator("cathide.apply", text='', icon='FILE_TICK')
        
        row = layout.row()
        row.label("Presets", icon='SETTINGS')
        rows = 1
        row = layout.row()
        row.template_list("CatHidePresetUIList", "", scene, "preset_cathide_list", scene, "cathide_preset_index")
        col = row.column(align=True)
        col.operator("cathide.presetadd", text='', icon='ZOOMIN')
        if len(prlist)>=1 and (idx+1) <= len(prlist):
            col.operator("cathide.presetdelete", text='', icon='ZOOMOUT')
            col.operator("cathide.presetclear", text='', icon='X')
            col.separator()
            col.operator("cathide.applypreset", text='', icon='FILE_TICK')
            col.separator()
            if scene.cathide_show_presetdetails==True:
                col.prop(scene, "cathide_show_presetdetails", text="",icon='ZOOM_OUT')
            else:
                col.prop(scene, "cathide_show_presetdetails", text="",icon='ZOOM_IN')
            if scene.cathide_show_presetdetails==True:
                row = layout.row()
                row.label('Preset Details - ' + prlist[idx].name , icon='VIEWZOOM')
                row = layout.row()
                col = row.column(align=True)
                for p in activelist:
                    if p!="":
                        col.label(p, icon='CHECKBOX_HLT')
                col = row.column(align=True)
                for p in unactivelist:
                    if p!="":
                        col.label(p, icon='CHECKBOX_DEHLT')
            
                
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

# add preset operator
class CathidePresetAdd(bpy.types.Operator):
    bl_idname = "cathide.presetadd"
    bl_label = "Add Preset"
    bl_description = "Add CatHide Preset"
    bl_options = {'REGISTER', 'UNDO'}
        
    def execute(self, context):
        scene=bpy.context.scene
        plist=scene.panel_cathide_list
        prlist=scene.preset_cathide_list
        activelist=[]
        unactivelist=[]
                
        tempstr=""              
        #get list of active
        for p in plist:
            if p.panelstate==True:
                activelist.append(p.name)
        #store list in csv string
        for n in activelist:
            tempstr=tempstr + ",," + str(n)
        #reformat
           
        #add to prop
        newcat=prlist.add()
        newcat.activepanel=tempstr
            
        tempstr=""
        #get list of unactive
        for p in plist:
            if p.panelstate==False:
                unactivelist.append(p.name)
        #store list in csv string
        for n in unactivelist:
            tempstr=tempstr + ",," + str(n)
        #add to prop
        newcat.unactivepanel=tempstr
        newcat.name="Cathide Preset"
                                                            
        info = 'Preset Added'
        self.report({'INFO'}, info)
        
        return {'FINISHED'}
    
# delete preset operator
class CathidePresetDelete(bpy.types.Operator):
    bl_idname = "cathide.presetdelete"
    bl_label = "Delete Preset"
    bl_description = "Delete selected CatHide Preset"
    bl_options = {'REGISTER', 'UNDO'}
        
    def execute(self, context):
        scene=bpy.context.scene
        prlist=scene.preset_cathide_list
        idx=scene.cathide_preset_index
        
        if len(prlist)>=1 and (idx+1) <= len(prlist):
            prlist.remove(idx)
                                                                
            info = 'Preset Deleted'
            self.report({'INFO'}, info)
        else:
            info = 'Please select a Preset'
            self.report({'ERROR'}, info) 
        
        return {'FINISHED'}

# clear all preset operator
class CathidePresetClear(bpy.types.Operator):
    bl_idname = "cathide.presetclear"
    bl_label = "Clear All Preset"
    bl_description = "Delete All CatHide Preset"
    bl_options = {'REGISTER', 'UNDO'}
        
    def execute(self, context):
        scene=bpy.context.scene
        prlist=scene.preset_cathide_list
        idx=scene.cathide_preset_index
        
        if len(prlist)>=1:
            for i in range(len(prlist)-1,-1,-1):
                prlist.remove(i)
            
            info = 'Presets Cleared'
            self.report({'INFO'}, info)
        else:
            info = 'No Presets Saved'
            self.report({'ERROR'}, info)
        
        return {'FINISHED'}

# Apply preset operator
class CathideApplyPreset(bpy.types.Operator):
    bl_idname = "cathide.applypreset"
    bl_label = "Clear All Preset"
    bl_description = "Apply selected Cathide Preset"
    bl_options = {'REGISTER', 'UNDO'}
        
    def execute(self, context):
        scene=bpy.context.scene
        plist=scene.panel_cathide_list
        prlist=scene.preset_cathide_list
        idx=scene.cathide_preset_index
        activelist=[]
        unactivelist=[]
        
        #get formated lists
        if len(prlist)>=1 and (idx+1) <= len(prlist):
            tmp1=prlist[idx].activepanel.split(",,")
            tmp2=prlist[idx].unactivepanel.split(",,")
            for p in tmp1:
                activelist.append(p)
            for p in tmp2:
                unactivelist.append(p)
        #apply active
            for p in activelist:
                if p!="":
                    print(p)
                    for p2 in plist:
                        if p==p2.name:
                            p2.panelstate=True
        #apply unactive
            for p in unactivelist:
                if p!="":
                    print(p)
                    for p2 in plist:
                        if p==p2.name:
                            p2.panelstate=False
        #apply config to panels 
            bpy.ops.cathide.apply()
            
            info = 'Preset Applied'
            self.report({'INFO'}, info)
        
        else:
            info = 'Please select a Preset'
            self.report({'ERROR'}, info)
    
        return {'FINISHED'}

# Create custom property group
class CatHidePanelList(bpy.types.PropertyGroup):
    '''name = StringProperty() '''
    panelstate = bpy.props.BoolProperty(name="panelstate", default = True)
    
class CatHidePresetList(bpy.types.PropertyGroup):
    '''name = StringProperty(default = "Cathide Preset")'''
    activepanel = bpy.props.StringProperty(name="activepanel")
    unactivepanel = bpy.props.StringProperty(name="unactivepanel")
    


# -------------------------------------------------------------------
# register
# -------------------------------------------------------------------

def register():
    bpy.utils.register_class(CatHideUIList)
    bpy.utils.register_class(CatHidePresetUIList)
    bpy.utils.register_class(CatHidePanel)
    bpy.utils.register_class(CathideRefresh)
    bpy.utils.register_class(CathideApply)
    bpy.utils.register_class(CathidePresetAdd)
    bpy.utils.register_class(CathidePresetDelete)
    bpy.utils.register_class(CathidePresetClear)
    bpy.utils.register_class(CathideApplyPreset)
    bpy.utils.register_class(CatHidePanelList)
    bpy.types.Scene.panel_cathide_list = \
        bpy.props.CollectionProperty(type=CatHidePanelList)
    bpy.types.Scene.cathide_index = IntProperty()
    bpy.utils.register_class(CatHidePresetList)
    bpy.types.Scene.preset_cathide_list = \
        bpy.props.CollectionProperty(type=CatHidePresetList)
    bpy.types.Scene.cathide_preset_index = IntProperty()
    bpy.types.Scene.cathide_show_presetdetails = BoolProperty()

def unregister():
    bpy.utils.unregister_class(CatHideUIList)
    bpy.utils.unregister_class(CatHidePresetUIList)
    bpy.utils.unregister_class(CatHidePanel)
    bpy.utils.unregister_class(CathideRefresh)
    bpy.utils.unregister_class(CathideApply)
    bpy.utils.unregister_class(CathidePresetAdd)
    bpy.utils.unregister_class(CathidePresetDelete)
    bpy.utils.unregister_class(CathidePresetClear)
    bpy.utils.unregister_class(CathideApplyPreset)
    bpy.utils.unregister_class(CatHidePanelList)
    del bpy.types.Scene.panel_cathide_list
    bpy.utils.unregister_class(CatHidePresetList)
    del bpy.types.Scene.preset_cathide_list
    del bpy.types.Scene.cathide_index
    del bpy.typse.Scene.cathide_preset_index
    del bpy.typse.Scene.cathide_show_presetdetails
    
if __name__ == "__main__":
    register()
