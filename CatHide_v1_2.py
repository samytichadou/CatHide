# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; version 3
#  of the License.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####


bl_info = {  
 "name": "CatHide",  
 "author": "Samy Tichadou (tonton)",  
 "version": (1, 3),  
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
        if item.name=="Tools":
            layout.label(item.name)
        else:     
            layout.label(item.name)       
            if item.panelstate==False:
                if item.keep_cat_hidden==True:
                    layout.prop(item, "keep_cat_hidden", text='', icon="PINNED", emboss=True)
                else:
                    layout.prop(item, "keep_cat_hidden", text='', icon="UNPINNED", emboss=True)
            layout.prop(item, "panelstate", text="", emboss=True)
                   
class CatHideSpecificUIList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, flt_flag):
        scene=bpy.context.scene
        plist=scene.cathide_panel_list
        idx=scene.cathide_index
        
        if item.parent_category==plist[idx].name:
            if item.name=="Hide Panel":
                layout.label(item.name)
            else:
                layout.label(item.name)
                if item.specific_panel_state==False:
                    if item.keep_panel_hidden==True:
                        layout.prop(item, "keep_panel_hidden", text="", icon='PINNED', emboss=True)
                    else:
                        layout.prop(item, "keep_panel_hidden", text="", icon='UNPINNED', emboss=True)
                    layout.prop(item, "specific_panel_state", text="", emboss=True)
                else:
                    layout.prop(item, "specific_panel_state", text="", emboss=True)
        else:
            layout.enabled = False
            layout.label(item.name)
        
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
        plist=scene.cathide_panel_list
        prlist=scene.cathide_preset_list
        slist=scene.cathide_specific_panel_list
        idx=scene.cathide_preset_index
        sidx=scene.cathide_specific_index
        activecatlist=[]
        unactivecatlist=[]
        unactivepanellist=[]
        hiddencat=[]
        hiddenpanel=[]
        
        #get presets details
        if len(prlist)>=1 and (idx+1) <= len(prlist):
            tmp1=prlist[idx].activecat.split(",,")
            tmp2=prlist[idx].unactivecat.split(",,")
            for p in tmp1:
                activecatlist.append(p)
            for p in tmp2:
                unactivecatlist.append(p)
            tmp2=prlist[idx].unactivespanel.split(",,")
            for p in tmp2:
                unactivepanellist.append(p)
            tmp3=prlist[idx].pinhiddencat.split(",,")
            for p in tmp3:
                hiddencat.append(p)
            tmp4=prlist[idx].pinhiddenpanel.split(",,")
            for p in tmp4:
                hiddenpanel.append(p)
        
        row = layout.row()
        row.label("CATEGORIES", icon='MENU_PANEL')
        row = layout.row()
        row.template_list("CatHideUIList", "", scene, "cathide_panel_list", scene, "cathide_index", rows=7)
        col = row.column(align=True)
        col.operator("cathide.refresh", text='', icon='FILE_REFRESH')
        col.operator("cathide.apply", text='', icon='FILE_TICK')
        col.separator()
        col.operator("cathide.resetcatonly", text='', icon='CHECKBOX_HLT')
        
        row = layout.row()
        row = layout.row()
        row.prop(scene, "cathide_show_specific", text="PANELS",icon='COLLAPSEMENU')
        if scene.cathide_show_specific==True:
            row = layout.row()
            row.template_list("CatHideSpecificUIList", "", scene, "cathide_specific_panel_list", scene, "cathide_specific_index", rows=5)
            col = row.column(align=True)
            col.operator("cathide.refresh", text='', icon='FILE_REFRESH')
            col.operator("cathide.applyspecific", text='', icon='FILE_TICK')
            col.separator()
            col.operator("cathide.resetpanelonly", text='', icon='CHECKBOX_HLT')
            row = layout.row()
            col = row.column(align=True)
            if scene.cathide_show_specific_details==True:
                col.prop(scene, "cathide_show_specific_details", text="Panel Details - " + slist[sidx].name, icon='ZOOM_OUT')
                if len(slist)>=1 and (sidx+1) <= len(slist):
                    
                    if slist[sidx].panel_context=="":
                        col.label('Context : None')            
                    else:
                        col.label('Context : ' + slist[sidx].panel_context)
                    if slist[sidx].panel_module=="":
                        col.label('Module : None')  
                    else:
                        col.label('Module : ' + slist[sidx].panel_module)                        
            if scene.cathide_show_specific_details==False:
                col.prop(scene, "cathide_show_specific_details", text="Panel Details - " + slist[sidx].name, icon='ZOOM_IN')
            
        
        row = layout.row()
        if scene.cathide_show_preset==True or scene.cathide_show_specific==True:
            row = layout.row()
        row.prop(scene, "cathide_show_preset", text="PRESETS",icon='SETTINGS')
        if scene.cathide_show_preset==True:
            rows = 1
            row = layout.row()
            row.template_list("CatHidePresetUIList", "", scene, "cathide_preset_list", scene, "cathide_preset_index", rows=3)
            col = row.column(align=True)
            col.operator("cathide.presetadd", text='', icon='ZOOMIN')
            if len(prlist)>=1 and (idx+1) <= len(prlist):
                col.operator("cathide.presetdelete", text='', icon='ZOOMOUT')
                col.operator("cathide.presetclear", text='', icon='X')
                col.separator()
                col.operator("cathide.applypreset", text='', icon='FILE_TICK')
                row = layout.row()
                row.prop(scene, "cathide_show_presetcatdetails", text="Preset Categories - " + prlist[idx].name, icon='MENU_PANEL')
                if scene.cathide_show_presetcatdetails==True:
                    row = layout.row()
                    col = row.column(align=True)
                    for p in activecatlist:
                        if p!="":
                            col.label(p, icon='CHECKBOX_HLT')
                    col = row.column(align=True)
                    if prlist[idx].unactivecat=="":
                        col.label("No Hidden Category")
                    else:
                        for p in unactivecatlist:
                            if p!="":
                                col.label(p, icon='CHECKBOX_DEHLT')
                row = layout.row()
                row.prop(scene, "cathide_show_presetspaneldetails", text="Preset Panels - " + prlist[idx].name, icon='COLLAPSEMENU')
                if scene.cathide_show_presetspaneldetails==True:
                    row = layout.row()
                    col = row.column(align=True)
                    col.label("HIDDEN", icon='CHECKBOX_DEHLT')
                    if unactivepanellist=="":
                        col.label("No Hidden Panel")
                    else:
                        for p in unactivepanellist:
                            for p2 in hiddenpanel:
                                if p==p2 and p!="":
                                    col.label(p, icon='PINNED')
                        for p in (Counter(unactivepanellist)-Counter(hiddenpanel)):
                            if p!="":
                                col.label(p, icon='UNPINNED')
                    col = row.column(align=True)
                    col.label("SHOWED", icon='CHECKBOX_HLT')
                    if hiddenpanel=="":
                        col.label("No Showed Pinned Panel")
                    else:
                        if len((Counter(hiddenpanel)-Counter(unactivepanellist)))>0:
                            for p in (Counter(hiddenpanel)-Counter(unactivepanellist)):
                                if p!="":
                                    col.label(p, icon='PINNED')
                        else:
                            col.label("No Showed Pinned Panel")
                    


            
                
# refresh cathide collection
class CathideRefresh(bpy.types.Operator):
    bl_idname = "cathide.refresh"
    bl_label = "Refresh"
    bl_description = "Refresh Panel to Hide"
        
    def execute(self, context):
        scene=bpy.context.scene
        plist=scene.cathide_panel_list
        slist=scene.cathide_specific_panel_list
        tempstr1=""
        tempstr2=""
        registerexception=[]
        registerexception2=[]
        
        #get specific exception:
        for s in slist:
            if s.keep_panel_hidden==True:
                registerexception.append(s.name)
        for s in plist:
            if s.keep_cat_hidden==True:
                registerexception2.append(s.name)
        
        
        #clear panel list
        for i in range(len(plist)-1,-1,-1):
            plist.remove(i)
        #clear specific panel list
        for i in range(len(slist)-1,-1,-1):
            slist.remove(i)
        
        #declare category list
        catlistreg1=[]
        catlistreg2=[]
        catlistunreg1=[]
        catlistunreg2=[]
        catlistunreg3=[]
        panlistreg=[]
        panlistunreg=[]
        panregcon=[]
        panregmod=[]
        panunregcon=[]
        panunregmod=[]
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
            
        #get specific panels
        for n in plist:
            del panlistreg[:]
            del panlistunreg[:]
            del panregcon[:]
            del panunregcon[:]
            del panregmod[:]
            del panunregmod[:]
            for panel in bpy.types.Panel.__subclasses__():
                if hasattr(panel, 'bl_space_type'):
                    if hasattr(panel, 'bl_region_type'):
                        if hasattr(panel, 'bl_category'):
                            if panel.bl_space_type=="VIEW_3D":
                                if panel.bl_region_type=="TOOLS":
                                    if panel.bl_category == n.name:
                                        if "bl_rna" in panel.__dict__:
                                            panlistreg.append(panel.bl_label)
                                        elif "bl_rna" not in panel.__dict__:
                                            panlistunreg.append(panel.bl_label)
                                                                
            # add panels in collection
            for p in list(set(panlistreg)):
                newpan=slist.add()
                newpan.name=p
                newpan.parent_category=n.name
                newpan.specific_panel_state=True
                for panel in bpy.types.Panel.__subclasses__():
                    if hasattr(panel, 'bl_space_type'):
                        if hasattr(panel, 'bl_region_type'):
                            if hasattr(panel, 'bl_category'):
                                if hasattr(panel, 'bl_label'):
                                    if panel.bl_space_type=="VIEW_3D":
                                        if panel.bl_region_type=="TOOLS":
                                            if panel.bl_label == p:
                                                newpan.panel_module=panel.__module__
                                                if hasattr(panel, 'bl_context'):
                                                    newpan.panel_context=panel.bl_context
                            
            for p2 in list(set(panlistunreg)):
                newpan2=slist.add()
                newpan2.name=p2
                newpan2.parent_category=n.name
                newpan2.specific_panel_state=False
                for panel in bpy.types.Panel.__subclasses__():
                    if hasattr(panel, 'bl_space_type'):
                        if hasattr(panel, 'bl_region_type'):
                            if hasattr(panel, 'bl_category'):
                                if hasattr(panel, 'bl_label'):
                                    if panel.bl_space_type=="VIEW_3D":
                                        if panel.bl_region_type=="TOOLS":
                                            if panel.bl_label == p2:
                                                newpan.panel_module=panel.__module__
                                                if hasattr(panel, 'bl_context'):
                                                    newpan.panel_context=panel.bl_context
        
        # re-apply pinned hidden
        for s in slist:
            for e in registerexception:
                if s.name==e:
                    s.keep_panel_hidden=True
        for s in plist:
            for e in registerexception2:
                if s.name==e:
                    s.keep_cat_hidden=True
            
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
        plist=scene.cathide_panel_list
        slist=scene.cathide_specific_panel_list
        toregister=[]
        tounregister=[]
        registerexception=[]
        registerexception2=[]
                
        #get specific exception:
        for s in slist:
            if s.specific_panel_state==False:
                if s.keep_panel_hidden==True:
                    registerexception.append(s.name)
        for s in plist:
            if s.panelstate==False:
                if s.keep_cat_hidden==True:
                    registerexception2.append(s.name)
        #register cat
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
        #unregister cat
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
                                                                                            
        #unregister specific cat exception
        for e in registerexception2:
            for panel in bpy.types.Panel.__subclasses__():
                if hasattr(panel, 'bl_space_type'):
                    if hasattr(panel, 'bl_region_type'):
                        if hasattr(panel, 'bl_category'):
                            if panel.bl_space_type=="VIEW_3D":
                                if panel.bl_region_type=="TOOLS":
                                    if panel.bl_category==e:
                                        if "bl_rna" in panel.__dict__:
                                            bpy.utils.unregister_class(panel)
                                            
        #unregister specific panel exception
        for e in registerexception:
            for panel in bpy.types.Panel.__subclasses__():
                if hasattr(panel, 'bl_space_type'):
                    if hasattr(panel, 'bl_region_type'):
                        if hasattr(panel, 'bl_category'):
                            if hasattr(panel, 'bl_label'):
                                if panel.bl_space_type=="VIEW_3D":
                                    if panel.bl_region_type=="TOOLS":
                                        if panel.bl_label==e:
                                            if "bl_rna" in panel.__dict__:
                                                bpy.utils.unregister_class(panel)

        bpy.ops.cathide.refresh()
        
        for s in slist:
            for e in registerexception:
                if s.name==e:
                    s.keep_panel_hidden=True
        for s in plist:
            for e in registerexception2:
                if s.name==e:
                    s.keep_panel_hidden=True
                                                            
        info = 'Tool Shelf Categories Configuration applied'
        self.report({'INFO'}, info)
        
        return {'FINISHED'} 
    
# apply specific panel cathide configuration
class CathideApplySpecific(bpy.types.Operator):
    bl_idname = "cathide.applyspecific"
    bl_label = "Apply Specific Panels"
    bl_description = "Apply and Hide Specific Panels for selected category"
        
    def execute(self, context):
        scene=bpy.context.scene
        plist=scene.cathide_panel_list
        idx=scene.cathide_index
        slist=scene.cathide_specific_panel_list
        sptoregister=[]
        sptounregister=[]
        nok=plist[idx].name
                                            
        #register panels
        for p in slist:
            if p.specific_panel_state==True:
                sptoregister.append(p.name)
                
        for p in sptoregister:
            for panel in bpy.types.Panel.__subclasses__():
                if hasattr(panel, 'bl_space_type'):
                    if hasattr(panel, 'bl_region_type'):
                        if hasattr(panel, 'bl_category'):
                            if hasattr(panel, 'bl_label'):
                                if panel.bl_space_type=="VIEW_3D":
                                    if panel.bl_region_type=="TOOLS":
                                        if panel.bl_category==nok:
                                            if panel.bl_label==p:
                                                if "bl_rna" not in panel.__dict__:
                                                    bpy.utils.register_class(panel)
        #unregister panels
        for p in slist:
            if p.specific_panel_state==False:
                sptounregister.append(p.name)
                
        for p in sptounregister:
            for panel in bpy.types.Panel.__subclasses__():
                if hasattr(panel, 'bl_space_type'):
                    if hasattr(panel, 'bl_region_type'):
                        if hasattr(panel, 'bl_category'):
                            if hasattr(panel, 'bl_label'):
                                if panel.bl_space_type=="VIEW_3D":
                                    if panel.bl_region_type=="TOOLS":
                                        if panel.bl_category==nok:
                                            if panel.bl_label==p:
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
        plist=scene.cathide_panel_list
        prlist=scene.cathide_preset_list
        slist=scene.cathide_specific_panel_list
        activelist=[]
        unactivelist=[]
        hiddenpanel=[]
        hiddencat=[]
                        
        #get list of active cat
        tempstr=""   
        for p in plist:
            if p.panelstate==True:
                activelist.append(p.name)
        #store list in csv string
        for n in activelist:
            tempstr=tempstr + ",," + str(n)
        #reformat
           
        #add to prop
        newcat=prlist.add()
        newcat.name="Cathide Preset"
        newcat.activecat=tempstr
            
        #get list of unactive cat
        tempstr=""
        for p in plist:
            if p.panelstate==False:
                unactivelist.append(p.name)
        #store list in csv string
        for n in unactivelist:
            tempstr=tempstr + ",," + str(n)
        #add to prop
        newcat.unactivecat=tempstr
                                                                    
        info = 'Preset Added'
        self.report({'INFO'}, info)
        
        #clear lists
        del unactivelist[:]
                
        #get list of unactive specific panels
        tempstr=""
        for p in slist:
            if p.specific_panel_state==False:
                unactivelist.append(p.name)
        #store list in csv string
        for n in unactivelist:
            tempstr=tempstr + ",," + str(n)
        #add to prop
        newcat.unactivespanel=tempstr
        
        #get list of pin hidden panels
        tempstr=""
        for p in slist:
            if p.keep_panel_hidden==True:
                hiddenpanel.append(p.name)
        #store list in csv string
        for n in hiddenpanel:
            tempstr=tempstr + ",," + str(n)
        #add to prop
        newcat.pinhiddenpanel=tempstr
        
        #get list of pin hidden cat
        tempstr=""
        for p in plist:
            if p.keep_cat_hidden==True:
                hiddencat.append(p.name)
        #store list in csv string
        for n in hiddencat:
            tempstr=tempstr + ",," + str(n)
        #add to prop
        newcat.pinhiddencat=tempstr
                                                            
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
        prlist=scene.cathide_preset_list
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
        prlist=scene.cathide_preset_list
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
        plist=scene.cathide_panel_list
        prlist=scene.cathide_preset_list
        slist=scene.cathide_specific_panel_list
        idx=scene.cathide_preset_index
        activecatlist=[]
        unactivecatlist=[]
        activepanellist=[]
        unactivepanellist=[]
        hiddencat=[]
        hiddenpanel=[]
        
        bpy.ops.cathide.refresh()
        
        #get formated lists
        if len(prlist)>=1 and (idx+1) <= len(prlist):
            tmp1=prlist[idx].activecat.split(",,")
            tmp2=prlist[idx].unactivecat.split(",,")
            tmp3=prlist[idx].unactivespanel.split(",,")
            tmp4=prlist[idx].pinhiddencat.split(",,")
            tmp5=prlist[idx].pinhiddenpanel.split(",,")
            for p in tmp1:
                activecatlist.append(p)
            for p in tmp2:
                unactivecatlist.append(p)
            for p in tmp3:
                unactivepanellist.append(p)
            for p in tmp4:
                hiddencat.append(p)
            for p in tmp5:
                hiddenpanel.append(p)
        #apply active cat
            for p in activecatlist:
                if p!="":
                    for p2 in plist:
                        if p==p2.name:
                            p2.panelstate=True
        #apply unactive cat
            for p in unactivecatlist:
                if p!="":
                    for p2 in plist:
                        if p==p2.name:
                            p2.panelstate=False
        #apply active panel
            for p in activepanellist:
                if p!="":
                    for p2 in slist:
                        if p==p2.name:
                            p2.specific_panel_state=True
        #apply unactive panel
            for p in unactivepanellist:
                if p!="":
                    for p2 in slist:
                        if p==p2.name:
                            p2.specific_panel_state=False
        #apply config to panels
            #register cat
            for p in plist:
                if p.panelstate==True:
                    for panel in bpy.types.Panel.__subclasses__():
                        if hasattr(panel, 'bl_space_type'):
                            if hasattr(panel, 'bl_region_type'):
                                if hasattr(panel, 'bl_category'):
                                    if panel.bl_space_type=="VIEW_3D":
                                        if panel.bl_region_type=="TOOLS":
                                            if panel.bl_category==p.name:
                                                if "bl_rna" not in panel.__dict__:
                                                    bpy.utils.register_class(panel)
            #unregister cat
            for p in plist:
                if p.panelstate==False:
                    for panel in bpy.types.Panel.__subclasses__():
                        if hasattr(panel, 'bl_space_type'):
                            if hasattr(panel, 'bl_region_type'):
                                if hasattr(panel, 'bl_category'):
                                    if panel.bl_space_type=="VIEW_3D":
                                        if panel.bl_region_type=="TOOLS":
                                            if panel.bl_category==p.name:
                                                if "bl_rna" in panel.__dict__:
                                                    bpy.utils.unregister_class(panel)
                                            
            # unregister panels
            for p in slist:
                if p.specific_panel_state==False:
                    for panel in bpy.types.Panel.__subclasses__():
                        if hasattr(panel, 'bl_space_type'):
                            if hasattr(panel, 'bl_region_type'):
                                if hasattr(panel, 'bl_category'):
                                    if hasattr(panel, 'bl_label'):
                                        if panel.bl_space_type=="VIEW_3D":
                                            if panel.bl_region_type=="TOOLS":
                                                if panel.bl_label==p.name:
                                                    if "bl_rna" in panel.__dict__:
                                                        bpy.utils.unregister_class(panel)
                                                        
            # Apply hidden pinnings 
            for s in slist:
                for e in hiddenpanel:
                    if s.name==e:
                        s.keep_panel_hidden=True
            for s in plist:
                for e in hiddencat:
                    if s.name==e:
                        s.keep_panel_hidden=True

            info = 'Preset Applied'
            self.report({'INFO'}, info)
        
        else:
            info = 'Please select a Preset'
            self.report({'ERROR'}, info)
    
        return {'FINISHED'}

# Reset Cathide Cat Only
class CathideResetCatOnly(bpy.types.Operator):
    bl_idname = "cathide.resetcatonly"
    bl_label = "Reset Categories Only"
    bl_description = "Reset Cathide Categories Only"
    bl_options = {'REGISTER', 'UNDO'}
        
    def execute(self, context):
        scene=bpy.context.scene
        plist=scene.cathide_panel_list
        
        for p in plist:
            if p.panelstate==False:
                if p.keep_cat_hidden!=True:
                    p.panelstate=True
        bpy.ops.cathide.apply()
                    
        info = 'Tool Shelf Categories Reset'
        self.report({'INFO'}, info)
    
        return {'FINISHED'}
    
# Reset Cathide Panel Only
class CathideResetPanelOnly(bpy.types.Operator):
    bl_idname = "cathide.resetpanelonly"
    bl_label = "Reset Panel Only"
    bl_description = "Reset Cathide Panel Only"
    bl_options = {'REGISTER', 'UNDO'}
        
    def execute(self, context):
        scene=bpy.context.scene
        slist=scene.cathide_specific_panel_list
        
        for p in slist:
            if p.specific_panel_state==False:
                if p.keep_panel_hidden!=True:
                    p.specific_panel_state=True
        bpy.ops.cathide.applyspecific()
                    
        info = 'Tool Shelf Panels Reset'
        self.report({'INFO'}, info)
    
        return {'FINISHED'}

# Create custom property group
class CatHidePanelList(bpy.types.PropertyGroup):
    '''name = StringProperty() '''
    panelstate = bpy.props.BoolProperty(name="panelstate", default = True)
    keep_cat_hidden = bpy.props.BoolProperty(name="keep_cat_hidden", description="PIN HIDDEN : If active, the Category will not be reset by other Actions",default = False)

class CatHideSpecificPanelList(bpy.types.PropertyGroup):
    '''name = StringProperty() '''
    parent_category = bpy.props.StringProperty(name="parent_category")
    specific_panel_state = bpy.props.BoolProperty(name="specific_panel_state", default = True)
    panel_context = bpy.props.StringProperty(name="panel_context")
    panel_module = bpy.props.StringProperty(name="panel_module")
    keep_panel_hidden = bpy.props.BoolProperty(name="keep_panel_hidden", description="PIN HIDDEN : If active, the Panel will not be reset by other Actions",default = False)
    
class CatHidePresetList(bpy.types.PropertyGroup):
    '''name = StringProperty(default = "Cathide Preset")'''
    activecat = bpy.props.StringProperty(name="activecat")
    unactivecat = bpy.props.StringProperty(name="unactivecat")
    unactivespanel = bpy.props.StringProperty(name="unactivespanel")
    pinhiddencat = bpy.props.StringProperty(name="pinhiddencat")
    pinhiddenpanel = bpy.props.StringProperty(name="pinhiddenpanel")
    
# -------------------------------------------------------------------
# register
# -------------------------------------------------------------------

def register():
    bpy.utils.register_class(CatHideUIList)
    bpy.utils.register_class(CatHideSpecificUIList)
    bpy.utils.register_class(CatHidePresetUIList)
    bpy.utils.register_class(CatHidePanel)
    bpy.utils.register_class(CathideRefresh)
    bpy.utils.register_class(CathideApply)
    bpy.utils.register_class(CathideApplySpecific)
    bpy.utils.register_class(CathidePresetAdd)
    bpy.utils.register_class(CathidePresetDelete)
    bpy.utils.register_class(CathidePresetClear)
    bpy.utils.register_class(CathideApplyPreset)
    bpy.utils.register_class(CathideResetCatOnly)
    bpy.utils.register_class(CathideResetPanelOnly)
    bpy.utils.register_class(CatHidePanelList)
    bpy.types.Scene.cathide_panel_list = \
        bpy.props.CollectionProperty(type=CatHidePanelList)
    bpy.types.Scene.cathide_index = IntProperty()
    bpy.utils.register_class(CatHideSpecificPanelList)
    bpy.types.Scene.cathide_specific_panel_list = \
        bpy.props.CollectionProperty(type=CatHideSpecificPanelList)
    bpy.types.Scene.cathide_specific_index = IntProperty()
    bpy.utils.register_class(CatHidePresetList)
    bpy.types.Scene.cathide_preset_list = \
        bpy.props.CollectionProperty(type=CatHidePresetList)
    bpy.types.Scene.cathide_preset_index = IntProperty()
    bpy.types.Scene.cathide_show_specific = BoolProperty()
    bpy.types.Scene.cathide_show_specific_details = BoolProperty()
    bpy.types.Scene.cathide_show_preset = BoolProperty()
    bpy.types.Scene.cathide_show_presetcatdetails = BoolProperty()
    bpy.types.Scene.cathide_show_presetspaneldetails = BoolProperty()

def unregister():
    bpy.utils.unregister_class(CatHideUIList)
    bpy.utils.unregister_class(CatHideSpecificUIList)
    bpy.utils.unregister_class(CatHidePresetUIList)
    bpy.utils.unregister_class(CatHidePanel)
    bpy.utils.unregister_class(CathideRefresh)
    bpy.utils.unregister_class(CathideApply)
    bpy.utils.unregister_class(CathideApplySpecific)
    bpy.utils.unregister_class(CathidePresetAdd)
    bpy.utils.unregister_class(CathidePresetDelete)
    bpy.utils.unregister_class(CathidePresetClear)
    bpy.utils.unregister_class(CathideApplyPreset)
    bpy.utils.unregister_class(CathideResetCatOnly)
    bpy.utils.unregister_class(CathideResetPanelOnly)
    bpy.utils.unregister_class(CatHidePanelList)
    del bpy.types.Scene.cathide_panel_list
    bpy.utils.unregister_class(CatHideSpecificPanelList)
    del bpy.types.Scene.cathide_specific_panel_list
    bpy.utils.unregister_class(CatHidePresetList)
    del bpy.types.Scene.cathide_preset_list
    del bpy.types.Scene.cathide_index
    del bpy.types.Scene.cathide_specific_index
    del bpy.types.Scene.cathide_preset_index
    del bpy.types.Scene.cathide_show_specific
    del bpy.types.Scene.cathide_show_specific_details
    del bpy.types.Scene.cathide_show_preset
    del bpy.types.Scene.cathide_show_presetcatdetails
    del bpy.types.Scene.cathide_show_presetspaneldetails
    
if __name__ == "__main__":
    register()