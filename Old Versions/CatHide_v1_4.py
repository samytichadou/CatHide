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
 "version": (1, 4),  
 "blender": (2, 7, 8),  
 "location": "3D View > ToolShelf > Tools",  
 "description": "Hide Toolshelf Category and N-Panels from 3D View",  
  "wiki_url": "https://github.com/samytichadou/CatHide-Addon-for-Blender/wiki",  
 "tracker_url": "https://github.com/samytichadou/CatHide-Addon-for-Blender/issues/new",  
 "category": "3D View"}

import bpy
from bpy.props import IntProperty, CollectionProperty , StringProperty , BoolProperty
from bpy.types import Panel
from collections import Counter
import datetime

# declare UILIST
class CatHideUIList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        if item.name=="Tools":
            layout.label(item.name)
        else:     
            layout.label(item.name)       
            if item.keep_cat_hidden==True:
                layout.prop(item, "keep_cat_hidden", text='', icon="PINNED", emboss=True)
            else:
                layout.prop(item, "keep_cat_hidden", text='', icon="UNPINNED", emboss=True)
            layout.prop(item, "panelstate", text="", emboss=True)
                   
class CatHideSpecificUIList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):

        if item.name=="Hide Panel":
            layout.label(item.name)
        else:
            layout.label(item.name)
            layout.prop(item, "specific_panel_state", text="", emboss=True)
        
class CatHidePresetUIList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        layout.prop(item, "name", text="", icon='SETTINGS',  emboss=False, translate=False)
        
class CatHideNUIList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        layout.label(item.name)       
        if item.pin_npanel==True:
            layout.prop(item, "pin_npanel", text='', icon="PINNED", emboss=True)
        else:
            layout.prop(item, "pin_npanel", text='', icon="UNPINNED", emboss=True)
        layout.prop(item, "n_panel_state", text="", emboss=True)
#cathide_npanel_list

# ui list actions
class CatHideListActions(bpy.types.Operator):
    bl_idname = "cathide.list_action"
    bl_label = "CatHide List Action"

    action = bpy.props.EnumProperty(
        items=(
            ('UP', "Up", ""),
            ('DOWN', "Down", ""),))

    def invoke(self, context, event):
        scn = bpy.context.scene
        idx = scn.cathide_index
        items = scn.cathide_panel_list
        try:
            item = scn.cathide_panel_list[idx]
        except IndexError:
            pass
        else:
            if self.action == 'DOWN' and idx < len(items) - 1:
                oidx=idx
                items.move(idx, idx+1)
                bpy.context.scene.cathide_index=oidx+1
                
            elif self.action == 'UP' and idx >= 1:
                oidx=idx
                items.move(idx, idx-1)
                bpy.context.scene.cathide_index=oidx-1
        return {"FINISHED"}
    
# draw the panel
class CatHidePanel(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Tools"
    bl_label = "CatHide"

    def draw(self, context):
        layout = self.layout
        scene=bpy.context.scene
        plist=scene.cathide_panel_list
        prlist=scene.cathide_preset_list
        slist=scene.cathide_specific_panel_list
        slist2=scene.cathide_temporary_panel_list
        nlist=scene.cathide_npanel_list
        catidx=scene.cathide_index
        idx=scene.cathide_preset_index
        sidx=scene.cathide_specific_index
        nidx=scene.cathide_npanel_index
        #declare lists
        activecatlist=[]
        unactivecatlist=[]
        activepanellist=[]
        unactivepanellist=[]
        hiddencat=[]
        catorderlist=[]
        NPorderlist=[]
        unactiveNPlist=[]

        
        #get presets details
        if len(prlist)>=1 and (idx+1) <= len(prlist):
            tmp1=prlist[idx].activecat.split(",,")
            tmp2=prlist[idx].unactivecat.split(",,")
            for p in tmp1:
                activecatlist.append(p)
            for p in tmp2:
                unactivecatlist.append(p)
            tmp3=prlist[idx].unactivespanel.split(",,")
            for p in tmp3:
                unactivepanellist.append(p)
            tmp6=prlist[idx].catorder.split(",,")
            for p in tmp6:
                catorderlist.append(p)
            tmp7=prlist[idx].activespanel.split(",,")
            for p in tmp7:
                activepanellist.append(p)
            tmp8=prlist[idx].npanelsorder.split(",,")
            for p in tmp8:
                NPorderlist.append(p)
            tmp9=prlist[idx].unactivesnpanel.split(",,")
            for p in tmp9:
                unactiveNPlist.append(p)
                
        row = layout.row()
        row.prop(scene, "cathide_show_toolshelfcat", text="TOOLSHELF CATEGORIES",icon='MENU_PANEL')
        if scene.cathide_show_toolshelfcat==True:
            row = layout.row()
            row.template_list("CatHideUIList", "", scene, "cathide_panel_list", scene, "cathide_index", rows=7)
            col = row.column(align=True)
            col.operator("cathide.list_action", icon='TRIA_UP', text="").action = 'UP'
            col.operator("cathide.list_action", icon='TRIA_DOWN', text="").action = 'DOWN'
            col.separator()
            col.operator("cathide.refresh", text='', icon='FILE_REFRESH')
            col.operator("cathide.apply", text='', icon='FILE_TICK')
            col.separator()
            col.operator("cathide.reset", text='', icon='CHECKBOX_HLT')
        
        row = layout.row()
        row.prop(scene, "cathide_show_specific", text="TOOLSHELF PANELS",icon='COLLAPSEMENU')
        if scene.cathide_show_specific==True:
            if len(plist)>=1 and (catidx+1) <= len(plist) and scene.cathide_show_toolshelfcat==False:
                row = layout.row()
                row.label("Category - " + plist[catidx].name)
            row = layout.row()
            row.template_list("CatHideSpecificUIList", "", scene, "cathide_temporary_panel_list", scene, "cathide_specific_index", rows=4)
            col = row.column(align=True)
            col.operator("cathide.refresh", text='', icon='FILE_REFRESH')
            col.operator("cathide.applyspecific", text='', icon='FILE_TICK')
            col.separator()
            col.operator("cathide.reset_specific", text='', icon='CHECKBOX_HLT')
            col.separator()
            if scene.cathide_show_onlycontext_specific==True:
                col.prop(scene, "cathide_show_onlycontext_specific", text="", icon="GHOST_DISABLED")
            else:
                col.prop(scene, "cathide_show_onlycontext_specific", text="", icon="GHOST_ENABLED")
            row = layout.row()
            col = row.column(align=True)
            if scene.cathide_show_specific_details==True:
                col.prop(scene, "cathide_show_specific_details", text="Panel Details - " + slist2[sidx].name, icon='ZOOM_OUT')
                if len(slist2)>=1 and (sidx+1) <= len(slist2):
                    if slist2[sidx].panel_context=="":
                        col.label('Context : None')            
                    else:
                        col.label('Context : ' + slist2[sidx].panel_context)
                    if slist2[sidx].panel_module=="":
                        col.label('Module : None')  
                    else:
                        col.label('Module : ' + slist2[sidx].panel_module)                        
            if scene.cathide_show_specific_details==False:
                if len(slist2)>=1 and (sidx+1) <= len(slist2):
                    col.prop(scene, "cathide_show_specific_details", text="Panel Details - " + slist2[sidx].name, icon='ZOOM_IN')
        
        row = layout.row()
        row.prop(scene, "cathide_show_npanels", text="N-PANELS",icon='SPLITSCREEN')
        if scene.cathide_show_npanels==True:
            row = layout.row()
            if scene.cathide_show_onlycontext_npanels==False:
                row.template_list("CatHideNUIList", "", scene, "cathide_npanel_list", scene, "cathide_npanel_index", rows=7)    
            else:
                row.template_list("CatHideNUIList", "", scene, "cathide_npanelnocontext_list", scene, "cathide_npanel_index", rows=7)
            col = row.column(align=True)
            col.separator()
            col.operator("cathide.refresh", text='', icon='FILE_REFRESH')
            col.operator("cathide.apply_npanels", text='', icon='FILE_TICK')
            col.separator()
            if scene.cathide_show_onlycontext_npanels==True:
                col.prop(scene, "cathide_show_onlycontext_npanels", text="", icon="GHOST_DISABLED")
            else:
                col.prop(scene, "cathide_show_onlycontext_npanels", text="", icon="GHOST_ENABLED")  
            row = layout.row()
            col = row.column(align=True)
            if scene.cathide_show_npanel_details==True:
                col.prop(scene, "cathide_show_npanel_details", text="N-Panel Details - " + nlist[nidx].name, icon='ZOOM_OUT')
                if len(slist2)>=1 and (sidx+1) <= len(slist2):
                    if slist2[sidx].panel_context=="":
                        col.label('Context : None')            
                    else:
                        col.label('Context : ' + nlist[nidx].n_panel_context)
                    if slist2[sidx].panel_module=="":
                        col.label('Module : None')  
                    else:
                        col.label('Module : ' + nlist[nidx].n_panel_module)
            if scene.cathide_show_npanel_details==False:
                if len(slist)>=1 and (sidx+1) <= len(slist):
                    col.prop(scene, "cathide_show_npanel_details", text="N-Panel Details - " + nlist[nidx].name, icon='ZOOM_IN')
                        
        row = layout.row()
        row.prop(scene, "cathide_show_preset", text="PRESETS",icon='SETTINGS')
        if scene.cathide_show_preset==True:
            rows = 1
            row = layout.row()
            row.template_list("CatHidePresetUIList", "", scene, "cathide_preset_list", scene, "cathide_preset_index", rows=5)
            col = row.column(align=True)
            col.operator("cathide.presetadd", text='', icon='ZOOMIN')
            if len(prlist)>=1 and (idx+1) <= len(prlist):
                col.operator("call.updatepresets_menu", text='', icon='PREFERENCES')
                col.operator("cathide.presetdelete", text='', icon='ZOOMOUT')
                col.operator("call.clearpresets_menu", text='', icon='X')
                col.separator()
                
                col.operator("cathide.loadpreset", text='', icon='LOAD_FACTORY')
                col.operator("cathide.applypreset", text='', icon='FILE_TICK')
                row = layout.row()
                row.prop(scene, "cathide_show_presetcatdetails", text="Preset Categories - " + prlist[idx].name, icon='MENU_PANEL')
                if scene.cathide_show_presetcatdetails==True:
                    row = layout.row()
                    col = row.column(align=True)
                    for p in catorderlist:
                        if p!="":
                            chk=0
                            for p2 in unactivecatlist:
                                if p==p2:
                                    chk=1
                            if chk==1:
                                col.label(p, icon='CHECKBOX_DEHLT')
                            elif chk==0:
                                col.label(p, icon='CHECKBOX_HLT')
                    
                row = layout.row()
                row.prop(scene, "cathide_show_presetspaneldetails", text="Preset Panels - " + prlist[idx].name, icon='COLLAPSEMENU')
                if scene.cathide_show_presetspaneldetails==True:
                    row = layout.row()
                    col = row.column(align=True)
                    if len(unactivepanellist)!=1:
                        col.label("PANELS", icon='COLLAPSEMENU')
                        for p in unactivepanellist:
                            if p != '':
                                p2=p.split("''")
                                col.label(p2[0], icon='CHECKBOX_DEHLT')
                        col = row.column(align=True)
                        col.label("FROM", icon='MENU_PANEL')
                        for p in unactivepanellist:
                            if p != '':
                                p2=p.split("''")
                                col.label(p2[3])
                        col = row.column(align=True)
                        col.label("CONTEXT", icon='EDITMODE_HLT')
                        for p in unactivepanellist:
                            if p != '':
                                p2=p.split("''")
                                if p2[1]=="":
                                    col.label("None")
                                else:
                                    col.label(p2[1])
                    else:
                        col.label("No Hidden Panel")
                
                row = layout.row()
                row.prop(scene, "cathide_show_presetsnpaneldetails", text="Preset N-Panels - " + prlist[idx].name, icon='MENU_PANEL')
                if scene.cathide_show_presetsnpaneldetails==True:
                    row = layout.row()
                    col = row.column(align=True)
                    for p in NPorderlist:
                        if p!="":
                            chk=0
                            for p2 in unactiveNPlist:
                                if p==p2:
                                    chk=1
                            if chk==1:
                                col.label(p, icon='CHECKBOX_DEHLT')
                            elif chk==0:
                                col.label(p, icon='CHECKBOX_HLT')
                
                        
                row = layout.row()
                row.prop(scene, "cathide_show_presetsutility", text="Preset Utility", icon='MODIFIER')
                if scene.cathide_show_presetsutility==True:
                    row = layout.row()
                    row.menu("CatHide_CopyPreset_ToScene", text='Copy to')
                    row.prop(scene, "cathide_copyallpresets", text='All Presets')

#update fonction for refresh panels UI
def update_specificpanel_list(self, context):
    bpy.ops.cathide.updatetemp()

#update fonction for refresh Npanels Ui no context
def update_npanelnocontext_list(self, context):
    bpy.ops.cathide.updatenocontext()
        
# refresh cathide collection
class CathideRefresh(bpy.types.Operator):
    bl_idname = "cathide.refresh"
    bl_label = "Refresh"
    bl_description = "Refresh Panel to Hide"
        
    def execute(self, context):
        scene=bpy.context.scene
        plist=scene.cathide_panel_list
        nlist=scene.cathide_npanel_list
        nlistnc=scene.cathide_npanelnocontext_list
        slist=scene.cathide_specific_panel_list
        slist2=scene.cathide_temporary_panel_list
        tempstr1=""
        tempstr2=""
        registerexception2=[]
        registerexceptionnpanel=[]
        registerexceptionnpanelnc=[]
        catlist=[]
        npanellist=[]
        npanelnclist=[]
                
        #get specific exception:
        for s in plist:
            catlist.append(s.name)
            if s.keep_cat_hidden==True:
                registerexception2.append(s.name)
                
        for s in nlist:
            npanellist.append(s.name)
            if s.pin_npanel==True:
                registerexceptionnpanel.append(s.name)
                
        for s in nlistnc:
            npanelnclist.append(s.name)
            if s.pin_npanel==True:
                registerexceptionnpanelnc.append(s.name)
        
        #clear specific panel list
        for i in range(len(slist)-1,-1,-1):
            slist.remove(i)
        
        #declare category list
        catorderlist1=[]
        catorderlist2=[]
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
        npanelreg1=[]
        npanelunreg1=[]
        npanelunreg2=[]
        npanelorderlist=[]
        npanelnocontext=[]
        
        #find category and append them in the lists
        for panel in bpy.types.Panel.__subclasses__():
            if hasattr(panel, 'bl_space_type'):
                if hasattr(panel, 'bl_region_type'):
                    if hasattr(panel, 'bl_category'):
                        if panel.bl_space_type=="VIEW_3D":
                            if panel.bl_region_type=="TOOLS":
                                if str(panel.bl_category) not in str(catorderlist2):
                                    catorderlist2.append(panel.bl_category)
        for panel in bpy.types.Panel.__subclasses__():
            if hasattr(panel, 'bl_space_type'):
                if hasattr(panel, 'bl_region_type'):
                    if hasattr(panel, 'bl_category'):
                        if panel.bl_space_type=="VIEW_3D":
                            if panel.bl_region_type=="TOOLS":
                                if "bl_rna" not in panel.__dict__:
                                    if str(panel.bl_category) not in str(catlistunreg2):
                                        catlistunreg2.append(panel.bl_category)
                                elif "bl_rna" in panel.__dict__:
                                    if str(panel.bl_category) not in str(catlistreg2):
                                        catlistreg2.append(panel.bl_category)
        
        #format lists
        l1=Counter(catlistreg2)
        l2=Counter(catlistunreg2)
        diff=l2-l1
        for c in list(diff.elements()):
            catlistunreg3.append(c)
        
        #add new cats
        for c in catorderlist2:
            chk=0
            for c2 in plist:
                if c==c2.name:
                    chk=1
            if chk==0:
                newcat=plist.add()
                newcat.name=c
                
        #delete old cats
        for c in plist:
            chk=0
            for c2 in catorderlist2:
                if c2==c.name:
                    chk=1
            if chk==0:
                for c3 in catlist:
                    if c.name==c3:
                        id=catlist.index(c3)
                plist.remove(id)
        
        #correct current state of categories
        for c in plist:
            c.panelstate=False
        
        for panel in bpy.types.Panel.__subclasses__():
            if hasattr(panel, 'bl_space_type'):
                if hasattr(panel, 'bl_region_type'):
                    if hasattr(panel, 'bl_category'):
                        if panel.bl_space_type=="VIEW_3D":
                            if panel.bl_region_type=="TOOLS":
                                for c in plist:
                                    if c.name==panel.bl_category:
                                        if "bl_rna" in panel.__dict__:
                                            c.panelstate=True
                                            
                                            
        #find N Panels and append them in the lists
        for panel in bpy.types.Panel.__subclasses__():
            if hasattr(panel, 'bl_space_type'):
                if hasattr(panel, 'bl_region_type'):
                    if panel.bl_space_type=="VIEW_3D":
                        if panel.bl_region_type=="UI":
                            if str(panel.bl_label) not in str(npanelorderlist):
                                npanelorderlist.append(panel.bl_label)
                                
        for panel in bpy.types.Panel.__subclasses__():
            if hasattr(panel, 'bl_space_type'):
                if hasattr(panel, 'bl_region_type'):
                    if panel.bl_space_type=="VIEW_3D":
                        if panel.bl_region_type=="UI":
                            if "bl_rna" not in panel.__dict__:
                                if str(panel.bl_label) not in str(npanelunreg1):
                                    npanelunreg1.append(panel.bl_label)
                                    if hasattr(panel, 'bl_context') or "poll" in panel.__dict__:
                                        pass
                                    else:
                                        npanelnocontext.append(panel.bl_label)
                            elif "bl_rna" in panel.__dict__:
                                if str(panel.bl_label) not in str(npanelreg1):
                                    npanelreg1.append(panel.bl_label)
                                    if hasattr(panel, 'bl_context') or "poll" in panel.__dict__:
                                        pass
                                    else:
                                        npanelnocontext.append(panel.bl_label)
                                        
        #format lists
        n1=Counter(npanelreg1)
        n2=Counter(npanelunreg1)
        diffn=n2-n1
        for c in list(diffn.elements()):
            npanelunreg2.append(c)
            
        #add new npanels
        for c in npanelorderlist:
            chk=0
            for c2 in nlist:
                if c==c2.name:
                    chk=1
            if chk==0:
                newcat=nlist.add()
                newcat.name=c
                
        for c in npanelnocontext:
            chk=0
            for c2 in nlistnc:
                if c==c2.name:
                    chk=1
            if chk==0:
                newcat=nlistnc.add()
                newcat.name=c

        #delete old npanels
        for c in nlist:
            chk=0
            for c2 in npanelorderlist:
                if c2==c.name:
                    chk=1
            if chk==0:
                for c3 in npanellist:
                    if c.name==c3:
                        id=npanellist.index(c3)
                        nlist.remove(id)
                for c4 in npanelnclist:
                    if c.name==c4:
                        idnc=npanelnclist.index(c4)
                        nlistnc.remove(idnc)
        
        for c in nlistnc:
            chk=0
            for c2 in npanelnocontext:
                if c2==c.name:
                    chk=1
            if chk==0:
                for c4 in npanelnclist:
                    if c.name==c4:
                        idnc=npanelnclist.index(c4)
                        nlistnc.remove(idnc)
        
        #correct current state of Npanels
        for c in nlist:
            c.n_panel_state=False
        for c in nlistnc:
            c.n_panel_state=False
        
        for panel in bpy.types.Panel.__subclasses__():
            if hasattr(panel, 'bl_space_type'):
                if hasattr(panel, 'bl_region_type'):
                    if panel.bl_space_type=="VIEW_3D":
                        if panel.bl_region_type=="UI":
                            for c in nlist:
                                if c.name==panel.bl_label:
                                    if "bl_rna" in panel.__dict__:
                                        c.n_panel_state=True
                            for c2 in nlistnc:
                                if c2.name==panel.bl_label:
                                    if "bl_rna" in panel.__dict__:
                                        c2.n_panel_state=True
        
        #get context and module
        for panel in bpy.types.Panel.__subclasses__():
            if hasattr(panel, 'bl_space_type'):
                if hasattr(panel, 'bl_region_type'):
                    if panel.bl_space_type=="VIEW_3D":
                        if panel.bl_region_type=="UI":
                            for c in nlist:
                                if c.name==panel.bl_label:
                                    if "__module__" in panel.__dict__:
                                        c.n_panel_module=panel.__module__
                                        if hasattr(panel, 'bl_context'):
                                            c.n_panel_context=panel.bl_context
                                        else:
                                            if "poll" in panel.__dict__:
                                                c.n_panel_context="poll function"
                                                
        #get context and module
        for panel in bpy.types.Panel.__subclasses__():
            if hasattr(panel, 'bl_space_type'):
                if hasattr(panel, 'bl_region_type'):
                    if panel.bl_space_type=="VIEW_3D":
                        if panel.bl_region_type=="UI":
                            for c in nlistnc:
                                if c.name==panel.bl_label:
                                    if "__module__" in panel.__dict__:
                                        c.n_panel_module=panel.__module__
                                        if hasattr(panel, 'bl_context'):
                                            c.n_panel_context=panel.bl_context
                                        else:
                                            if "poll" in panel.__dict__:
                                                c.n_panel_context="poll function"
                                        

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
                                            newpan=slist.add()
                                            newpan.name=panel.bl_label
                                            newpan.parent_category=n.name
                                            newpan.specific_panel_state=True
                                            newpan.panel_module=panel.__module__
                                            if hasattr(panel, 'bl_context'):
                                                newpan.panel_context=panel.bl_context
                                            elif "poll" in panel.__dict__:
                                                newpan.panel_context="poll function"
                                        elif "bl_rna" not in panel.__dict__:
                                            newpan=slist.add()
                                            newpan.name=panel.bl_label
                                            newpan.parent_category=n.name
                                            newpan.specific_panel_state=False
                                            newpan.panel_module=panel.__module__
                                            if hasattr(panel, 'bl_context'):
                                                newpan.panel_context=panel.bl_context
                                            elif "poll" in panel.__dict__:
                                                newpan.panel_context="poll function"
                                                                
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
                                                newpan2.panel_module=panel.__module__
                                                if hasattr(panel, 'bl_context'):
                                                    newpan2.panel_context=panel.bl_context
        
        # re-apply pinned hidden
        for s in plist:
            for e in registerexception2:
                if s.name==e:
                    s.keep_cat_hidden=True
                    
        for s in nlist:
            for e in registerexceptionnpanel:
                if s.name==e:
                    s.pin_npanel=True
                    
        # Pull changes to temporary list
        for p in slist2:
            for p2 in slist:
                if p.name==p2.name:
                    if p.panel_context==p2.panel_context:
                        if p.panel_module==p2.panel_module:
                            p.specific_panel_state=p2.specific_panel_state
                    
        bpy.ops.cathide.updatetemp()
            
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
        slist2=scene.cathide_temporary_panel_list
        toregister=[]
        orderlist=[]
        
        #save temporary panels details
        for p in slist2:
            for p2 in slist:
                if p.name==p2.name:
                    if p.panel_context==p2.panel_context:
                        if p.panel_module==p2.panel_module:
                            p2.specific_panel_state=p.specific_panel_state
        
        #get cat order:
        for c in plist:
            orderlist.append(c.name)
                
        #get cat to register
        for p in plist:
            if p.panelstate==True:
                toregister.append(p.name)
        
        #unregister all cat       
        for p in plist:
            for panel in bpy.types.Panel.__subclasses__():
                if hasattr(panel, 'bl_space_type'):
                    if hasattr(panel, 'bl_region_type'):
                        if hasattr(panel, 'bl_category'):
                            if panel.bl_space_type=="VIEW_3D":
                                if panel.bl_region_type=="TOOLS":
                                    if panel.bl_category==p.name:
                                        if "bl_rna" in panel.__dict__:
                                            bpy.utils.unregister_class(panel)

        #register cats in order        
        for p in orderlist:
            for panel in bpy.types.Panel.__subclasses__():
                if hasattr(panel, 'bl_space_type'):
                    if hasattr(panel, 'bl_region_type'):
                        if hasattr(panel, 'bl_category'):
                            if panel.bl_space_type=="VIEW_3D":
                                if panel.bl_region_type=="TOOLS":
                                    if panel.bl_category==p:
                                        for p2 in toregister:
                                            if p==p2:
                                                if "bl_rna" not in panel.__dict__:
                                                    bpy.utils.register_class(panel)
     
        bpy.ops.cathide.refresh()
        
        info = 'Tool Shelf Categories Configuration applied'
        self.report({'INFO'}, info)
        
        return {'FINISHED'} 
    
# apply cathide N Panels configuration
class CathideApplyNPanels(bpy.types.Operator):
    bl_idname = "cathide.apply_npanels"
    bl_label = "Apply N-Panels"
    bl_description = "Apply and Hide N-Panels"
        
    def execute(self, context):
        scene=bpy.context.scene
        nlist=scene.cathide_npanel_list
        nlistnc=scene.cathide_npanelnocontext_list
        contextsensitive=scene.cathide_show_onlycontext_npanels
        toregister=[]
        orderlist=[]
        
        #get npanels from nocontext list
        if contextsensitive==True:
            #save to specific panel list
            for p in nlistnc:
                for p2 in nlist:
                    if p.name==p2.name:
                        if p.n_panel_context==p2.n_panel_context:
                            if p.n_panel_module==p2.n_panel_module:
                                p2.n_panel_state=p.n_panel_state
                                p2.pin_npanel=p.pin_npanel
        elif contextsensitive==False:
            #save to specific panel list
            for p in nlist:
                for p2 in nlistnc:
                    if p.name==p2.name:
                        if p.n_panel_context==p2.n_panel_context:
                            if p.n_panel_module==p2.n_panel_module:
                                p2.n_panel_state=p.n_panel_state
                                p2.pin_npanel=p.pin_npanel
        
        #get cat order:
        for c in nlist:
            orderlist.append(c.name)
                
        #get cat to register
        for p in nlist:
            if p.n_panel_state==True:
                toregister.append(p.name)
        
        #unregister all N Panels       
        for p in nlist:
            for panel in bpy.types.Panel.__subclasses__():
                if hasattr(panel, 'bl_space_type'):
                    if hasattr(panel, 'bl_region_type'):
                        if panel.bl_space_type=="VIEW_3D":
                            if panel.bl_region_type=="UI":
                                if panel.bl_label==p.name:
                                    if "bl_rna" in panel.__dict__:
                                        bpy.utils.unregister_class(panel)

        #register N Panels in order        
        for p in orderlist:
            for panel in bpy.types.Panel.__subclasses__():
                if hasattr(panel, 'bl_space_type'):
                    if hasattr(panel, 'bl_region_type'):
                        if panel.bl_space_type=="VIEW_3D":
                            if panel.bl_region_type=="UI":
                                if panel.bl_label==p:
                                    for p2 in toregister:
                                        if p==p2:
                                            if "bl_rna" not in panel.__dict__:
                                                bpy.utils.register_class(panel)
     
        bpy.ops.cathide.refresh()
        
        info = 'N-Panels Configuration applied'
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
        slist2=scene.cathide_temporary_panel_list
        sptounregister=[]
        
        #check selected category
        if (idx+1)<=len(plist):
            nok=plist[idx].name
        else:
            nok="No_Panel"
        
        #save temporary panels details
        for p in slist2:
            for p2 in slist:
                if p.name==p2.name:
                    if p.panel_context==p2.panel_context:
                        if p.panel_module==p2.panel_module:
                            p2.specific_panel_state=p.specific_panel_state
        
        if (idx+1)<=len(plist):        
            for p in slist:
                #if plist[idx].panelstate==False and plist[idx].keep_cat_hidden==True:
                    #break
                #else:
                    #if p.specific_panel_state==True:
                        for panel in bpy.types.Panel.__subclasses__():
                            if hasattr(panel, 'bl_space_type'):
                                if hasattr(panel, 'bl_region_type'):
                                    if hasattr(panel, 'bl_category'):
                                        if hasattr(panel, 'bl_label'):
                                            if panel.bl_space_type=="VIEW_3D":
                                                if panel.bl_region_type=="TOOLS":
                                                    if panel.bl_category==nok:
                                                        if panel.bl_label==p.name:
                                                            #if panel.__module__==p.panel_module:
                                                                #if hasattr(panel, 'bl_context'):
                                                                    #if panel.bl_context==p.panel_context:
                                                                        if "bl_rna" not in panel.__dict__:
                                                                            bpy.utils.register_class(panel)
                                                                #else:
                                                                    #if "bl_rna" not in panel.__dict__:
                                                                        #bpy.utils.register_class(panel)

        #count panels
        if (idx+1)<=len(plist): 
            panelcount=0
            for panel in bpy.types.Panel.__subclasses__():
                if hasattr(panel, 'bl_space_type'):
                    if hasattr(panel, 'bl_region_type'):
                        if hasattr(panel, 'bl_category'):
                            if hasattr(panel, 'bl_label'):
                                if panel.bl_space_type=="VIEW_3D":
                                    if panel.bl_region_type=="TOOLS":
                                        if panel.bl_category==nok:
                                            panelcount=panelcount+1
        
        #unregister panels  
        if (idx+1)<=len(plist):     
            uncount=0   
            for p in slist:
                if plist[idx].panelstate==True and plist[idx].keep_cat_hidden==True and uncount==(panelcount-1):
                    break
                else:  
                    if p.specific_panel_state==False:
                        for panel in bpy.types.Panel.__subclasses__():
                            if hasattr(panel, 'bl_space_type'):
                                if hasattr(panel, 'bl_region_type'):
                                    if hasattr(panel, 'bl_category'):
                                        if hasattr(panel, 'bl_label'):
                                            if panel.bl_space_type=="VIEW_3D":
                                                if panel.bl_region_type=="TOOLS":
                                                    if panel.bl_category==nok:
                                                        if panel.bl_label==p.name:
                                                            if panel.__module__==p.panel_module:
                                                                if "bl_context" in str(panel.__dict__):
                                                                    if panel.bl_context==p.panel_context:
                                                                        if "bl_rna" in panel.__dict__:
                                                                            bpy.utils.unregister_class(panel)
                                                                            uncount=uncount+1
                                                                            
                                                                else:
                                                                    if "bl_rna" in panel.__dict__:
                                                                        bpy.utils.unregister_class(panel)
                                                                        uncount=uncount+1
                                                                       
                    else:
                        if plist[idx].panelstate==False and plist[idx].keep_cat_hidden==True:
                            for panel in bpy.types.Panel.__subclasses__():
                                if hasattr(panel, 'bl_space_type'):
                                    if hasattr(panel, 'bl_region_type'):
                                        if hasattr(panel, 'bl_category'):
                                            if hasattr(panel, 'bl_label'):
                                                if panel.bl_space_type=="VIEW_3D":
                                                    if panel.bl_region_type=="TOOLS":
                                                        if panel.bl_category==nok:
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
        slist2=scene.cathide_temporary_panel_list
        nlist=scene.cathide_npanel_list
        nlistnc=scene.cathide_npanelnocontext_list
        contextsensitive=scene.cathide_show_onlycontext_npanels
        activelist=[]
        unactivelist=[]
        allcat=[]
        allNP=[]
        
        #save npanels no context details
        if contextsensitive==True:
            #save to specific panel list
            for p in nlistnc:
                for p2 in nlist:
                    if p.name==p2.name:
                        if p.n_panel_context==p2.n_panel_context:
                            if p.n_panel_module==p2.n_panel_module:
                                p2.n_panel_state=p.n_panel_state
                                p2.pin_npanel=p.pin_npanel
        elif contextsensitive==False:
            #save to specific panel list
            for p in nlist:
                for p2 in nlistnc:
                    if p.name==p2.name:
                        if p.n_panel_context==p2.n_panel_context:
                            if p.n_panel_module==p2.n_panel_module:
                                p2.n_panel_state=p.n_panel_state
                                p2.pin_npanel=p.pin_npanel
        
        #save temporary panels details
        for p in slist2:
            for p2 in slist:
                if p.name==p2.name:
                    if p.panel_context==p2.panel_context:
                        if p.panel_module==p2.panel_module:
                            p2.specific_panel_state=p.specific_panel_state

        #get cat order
        tempstr=""   
        for p in plist:
            allcat.append(p.name)
        #store list in csv string
        for n in allcat:
            tempstr=tempstr + ",," + str(n)
        #add to prop
        newcat=prlist.add()
        newcat.name="Cathide Preset"
        newcat.catorder=tempstr
        
        #get list of active cat
        tempstr=""   
        for p in plist:
            if p.panelstate==True:
                activelist.append(p.name)
        #store list in csv string
        for n in activelist:
            tempstr=tempstr + ",," + str(n)
           
        #add to prop
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
        
        #clear lists
        del activelist[:]
        del unactivelist[:]
        
        #get NPanels order
        tempstr=""   
        for p in nlist:
            allNP.append(p.name)
        #store list in csv string
        for n in allNP:
            tempstr=tempstr + ",," + str(n)
        #add to prop
        newcat.npanelsorder=tempstr
                
        #get list of active npanels
        tempstr=""   
        for p in nlist:
            if p.n_panel_state==True:
                activelist.append(p.name)
        #store list in csv string
        for n in activelist:
            tempstr=tempstr + ",," + str(n)
           
        #add to prop
        newcat.activesnpanel=tempstr
            
        #get list of unactive npanels
        tempstr=""
        for p in nlist:
            if p.n_panel_state==False:
                unactivelist.append(p.name)
        #store list in csv string
        for n in unactivelist:
            tempstr=tempstr + ",," + str(n)
        #add to prop
        newcat.unactivesnpanel=tempstr
        
        #clear lists
        del activelist[:]
        del unactivelist[:]
                
        #get list of unactive specific panels
        tempstr=""
        for p in slist:
            chk=0
            for p2 in plist:
                if p2.name==p.parent_category and p2.panelstate==False:
                    chk=1
            if p.specific_panel_state==False and chk==0:
                tempstr=tempstr + ",," + p.name + "''" + p.panel_context + "''" + p.panel_module + "''" + p.parent_category
        #add to prop
        newcat.unactivespanel=tempstr
        
        #get list of active specific panels
        tempstr=""
        for p in slist:
            chk=0
            for p2 in plist:
                if p2.name==p.parent_category and p2.panelstate==True:
                    chk=1
            if p.specific_panel_state==True and chk==0:
                tempstr=tempstr + ",," + p.name + "''" + p.panel_context + "''" + p.panel_module + "''" + p.parent_category
        #add to prop
        newcat.activespanel=tempstr
        
        scene.cathide_preset_index=len(prlist)-1
        
        info = 'Preset Added'
        self.report({'INFO'}, info)
        
        return {'FINISHED'}
    
# update preset operator
class CathidePresetUpdate(bpy.types.Operator):
    bl_idname = "cathide.presetupdate"
    bl_label = "Update Preset"
    bl_description = "Update Selected CatHide Preset"
    bl_options = {'REGISTER', 'UNDO'}
        
    def execute(self, context):
        scene=bpy.context.scene
        plist=scene.cathide_panel_list
        prlist=scene.cathide_preset_list
        slist=scene.cathide_specific_panel_list
        slist2=scene.cathide_temporary_panel_list
        idx=scene.cathide_preset_index
        nlist=scene.cathide_npanel_list
        nlistnc=scene.cathide_npanelnocontext_list
        contextsensitive=scene.cathide_show_onlycontext_npanels
        activelist=[]
        unactivelist=[]
        allcat=[]
        allNP=[]
        
        #save npanels no context details
        if contextsensitive==True:
            #save to specific panel list
            for p in nlistnc:
                for p2 in nlist:
                    if p.name==p2.name:
                        if p.n_panel_context==p2.n_panel_context:
                            if p.n_panel_module==p2.n_panel_module:
                                p2.n_panel_state=p.n_panel_state
                                p2.pin_npanel=p.pin_npanel
        elif contextsensitive==False:
            #save to specific panel list
            for p in nlist:
                for p2 in nlistnc:
                    if p.name==p2.name:
                        if p.n_panel_context==p2.n_panel_context:
                            if p.n_panel_module==p2.n_panel_module:
                                p2.n_panel_state=p.n_panel_state
                                p2.pin_npanel=p.pin_npanel
        
        #save temporary panels details
        for p in slist2:
            for p2 in slist:
                if p.name==p2.name:
                    if p.panel_context==p2.panel_context:
                        if p.panel_module==p2.panel_module:
                            p2.specific_panel_state=p.specific_panel_state

        #get cat order
        tempstr=""   
        for p in plist:
            allcat.append(p.name)
        #store list in csv string
        for n in allcat:
            tempstr=tempstr + ",," + str(n)
        #add to prop
        newcat=prlist[idx]
        newcat.catorder=tempstr
                        
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
        
        #clear lists
        del activelist[:]
        del unactivelist[:]
        
        #get NPanels order
        tempstr=""   
        for p in nlist:
            allNP.append(p.name)
        #store list in csv string
        for n in allNP:
            tempstr=tempstr + ",," + str(n)
        #add to prop
        newcat.npanelsorder=tempstr
        
        #get list of active npanels
        tempstr=""   
        for p in nlist:
            if p.n_panel_state==True:
                activelist.append(p.name)
        #store list in csv string
        for n in activelist:
            tempstr=tempstr + ",," + str(n)
           
        #add to prop
        newcat.activesnpanel=tempstr
            
        #get list of unactive npanels
        tempstr=""
        for p in nlist:
            if p.n_panel_state==False:
                unactivelist.append(p.name)
        #store list in csv string
        for n in unactivelist:
            tempstr=tempstr + ",," + str(n)
        #add to prop
        newcat.unactivesnpanel=tempstr
        
        #clear lists
        del activelist[:]
        del unactivelist[:]
                
        #get list of unactive specific panels
        tempstr=""
        for p in slist:
            if p.specific_panel_state==False:
                tempstr=tempstr + ",," + p.name + "''" + p.panel_context + "''" + p.panel_module + "''" + p.parent_category
        #add to prop
        newcat.unactivespanel=tempstr
        
        #get list of active specific panels
        tempstr=""
        for p in slist:
            if p.specific_panel_state==True:
                tempstr=tempstr + ",," + p.name + "''" + p.panel_context + "''" + p.panel_module + "''" + p.parent_category
        #add to prop
        newcat.activespanel=tempstr
        
        info = 'Preset Updated'
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
            
            if idx>(len(prlist)-1):
                scene.cathide_preset_index=len(prlist)-1
                                                                
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
    bl_label = "Apply Preset"
    bl_description = "Apply selected Cathide Preset"
    bl_options = {'REGISTER', 'UNDO'}
        
    def execute(self, context):
        scene=bpy.context.scene
        plist=scene.cathide_panel_list
        prlist=scene.cathide_preset_list
        nlist=scene.cathide_npanel_list
        nlistnc=scene.cathide_npanelnocontext_list
        contextsensitive=scene.cathide_show_onlycontext_npanels
        slist=scene.cathide_specific_panel_list
        idx=scene.cathide_preset_index
        activecatlist=[]
        unactivecatlist=[]
        activepanellist=[]
        unactivepanellist=[]
        activenpanelslist=[]
        unactivenpanelslist=[]
        pinactivecat=[]
        pinunactivecat=[]
        pinactivenpanels=[]
        pinunactivenpanels=[]
        catorderlist=[]

        
        if len(prlist)>=1 and (idx+1) <= len(prlist):
            
            #unregister all cat       
            for p in plist:
                for panel in bpy.types.Panel.__subclasses__():
                    if hasattr(panel, 'bl_space_type'):
                        if hasattr(panel, 'bl_region_type'):
                            if hasattr(panel, 'bl_category'):
                                if panel.bl_space_type=="VIEW_3D":
                                    if panel.bl_region_type=="TOOLS":
                                        if panel.bl_category==p.name:
                                            if "bl_rna" in panel.__dict__:
                                                bpy.utils.unregister_class(panel)
                                                
            #get formated lists
            tmp1=prlist[idx].activecat.split(",,")
            tmp2=prlist[idx].unactivecat.split(",,")
            tmp3=prlist[idx].activespanel.split(",,")
            tmp4=prlist[idx].unactivespanel.split(",,")
            tmp7=prlist[idx].catorder.split(",,")
            tmp8=prlist[idx].activesnpanel.split(",,")
            tmp9=prlist[idx].unactivesnpanel.split(",,")
            for p in tmp1:
                activecatlist.append(p)
            for p in tmp2:
                unactivecatlist.append(p)
            for p in tmp3:
                activepanellist.append(p)
            for p in tmp4:
                unactivepanellist.append(p)
            for p in tmp7:
                catorderlist.append(p)
            for p in tmp8:
                activenpanelslist.append(p)
            for p in tmp9:
                unactivenpanelslist.append(p)
                    
            #get pinned cat and panels
            for p in plist:
                if p.keep_cat_hidden==True:
                    if p.panelstate==True:
                        pinactivecat.append(p.name)
                    else:
                        pinunactivecat.append(p.name)
            for p in nlist:
                if p.pin_npanel==True:
                    if p.n_panel_state==True:
                        pinactivenpanels.append(p.name)
                    else:
                        pinunactivenpanels.append(p.name)
                
            #delete prop lists
            if len(plist)>=1:
                for i in range(len(plist)-1,-1,-1):
                    plist.remove(i)
                    
            #Recreate cat list
            for p in catorderlist:
                if p!="":
                    chk=0
                    chk2=0
                    newcat=plist.add()
                    newcat.name=p
                    newcat.panelstate=True
                    for p2 in pinactivecat:
                        if p==p2:
                            chk=1
                    for p3 in pinunactivecat:
                        if p==p3:
                            chk2=1
                    if chk==0 and chk2==0:
                        for p4 in unactivecatlist:
                            if p==p4:
                                newcat.panelstate=False
                            newcat.keep_cat_hidden=False
                    elif chk==1 and chk2==0:
                        newcat.panelstate=True
                        newcat.keep_cat_hidden=True
                    elif chk==0 and chk2==1:
                        newcat.panelstate=False
                        newcat.keep_cat_hidden=True
        
            #apply active panel
            for p in slist:
                p.specific_panel_state=True
            for p in slist:
                for p2 in unactivepanellist:
                    if p2!="":
                        p4=p2.split("''")
                        if p.name==p4[0] and p.panel_context==p4[1] and p.panel_module==p4[2] and p.parent_category==p4[3]:
                            p.specific_panel_state=False
                                        
            #register cats in order        
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
    
            #unregister panel
            for e in slist:
                chk=0
                if e.specific_panel_state==False:
                    for panel in bpy.types.Panel.__subclasses__():
                        if hasattr(panel, 'bl_space_type'):
                            if hasattr(panel, 'bl_region_type'):
                                if hasattr(panel, 'bl_category'):
                                    if hasattr(panel, 'bl_label'):
                                        for n in pinactivecat:
                                            if e.parent_category==n:
                                                chk=1
                                        if chk==0:
                                            if panel.bl_space_type=="VIEW_3D":
                                                if panel.bl_region_type=="TOOLS":
                                                    if panel.bl_label==e.name and panel.__module__==e.panel_module and panel.bl_category==e.parent_category:
                                                        if hasattr(panel, 'bl_context'):
                                                            if panel.bl_context==e.panel_context:
                                                                if "bl_rna" in panel.__dict__:
                                                                    bpy.utils.unregister_class(panel)
                                                                    
            #set all N Panels unactive :
            for p in nlist:
                p.n_panel_state=False
            #activate good ones:
            for p in nlist:
                if p.name in activenpanelslist:
                    p.n_panel_state=True
            #reapply pined:
            for p in nlist:
                if p.name in pinactivenpanels:
                    p.n_panel_state=True
                elif p.name in pinunactivenpanels:
                    p.n_panel_state=False
            #unregister all:
            for p in nlist:
                for panel in bpy.types.Panel.__subclasses__():
                    if hasattr(panel, 'bl_space_type'):
                        if hasattr(panel, 'bl_region_type'):
                            if panel.bl_space_type=="VIEW_3D":
                                if panel.bl_region_type=="UI":
                                    if panel.bl_label==p.name:
                                        if "bl_rna" in panel.__dict__:
                                            bpy.utils.unregister_class(panel)
            #register good ones:
            for p in nlist:
                if p.n_panel_state==True:
                    for panel in bpy.types.Panel.__subclasses__():
                        if hasattr(panel, 'bl_space_type'):
                            if hasattr(panel, 'bl_region_type'):
                                if panel.bl_space_type=="VIEW_3D":
                                    if panel.bl_region_type=="UI":
                                        if panel.bl_label==p.name:
                                            if "bl_rna" not in panel.__dict__:
                                                bpy.utils.register_class(panel)
        
            bpy.ops.cathide.refresh()
            
            #save npanels no context details
            if contextsensitive==True:
                #save to specific panel list
                for p in nlistnc:
                    for p2 in nlist:
                        if p.name==p2.name:
                            if p.n_panel_context==p2.n_panel_context:
                                if p.n_panel_module==p2.n_panel_module:
                                    p2.n_panel_state=p.n_panel_state
                                    p2.pin_npanel=p.pin_npanel
            elif contextsensitive==False:
                #save to specific panel list
                for p in nlist:
                    for p2 in nlistnc:
                        if p.name==p2.name:
                            if p.n_panel_context==p2.n_panel_context:
                                if p.n_panel_module==p2.n_panel_module:
                                    p2.n_panel_state=p.n_panel_state
                                    p2.pin_npanel=p.pin_npanel

            info = 'Preset Applied'
            self.report({'INFO'}, info)
        
        else:
            info = 'Please select a Preset'
            self.report({'ERROR'}, info)
    
        return {'FINISHED'}
    
# Load without applying preset operator
class CathideLoadPreset(bpy.types.Operator):
    bl_idname = "cathide.loadpreset"
    bl_label = "Load Preset"
    bl_description = "Load selected Cathide Preset without applying it"
    bl_options = {'REGISTER', 'UNDO'}
        
    def execute(self, context):
        scene=bpy.context.scene
        plist=scene.cathide_panel_list
        prlist=scene.cathide_preset_list
        slist=scene.cathide_specific_panel_list
        slist2=scene.cathide_temporary_panel_list
        nlist=scene.cathide_npanel_list
        nlistnc=scene.cathide_npanelnocontext_list
        contextsensitive=scene.cathide_show_onlycontext_npanels
        idx=scene.cathide_preset_index
        activecatlist=[]
        unactivecatlist=[]
        activepanellist=[]
        unactivepanellist=[]
        activenpanelslist=[]
        unactivenpanelslist=[]
        pinactivenpanels=[]
        pinunactivenpanels=[]
        pinactivecat=[]
        pinunactivecat=[]
        catorderlist=[]

        
        if len(prlist)>=1 and (idx+1) <= len(prlist):
                                                
            #get formated lists
            tmp1=prlist[idx].activecat.split(",,")
            tmp2=prlist[idx].unactivecat.split(",,")
            tmp3=prlist[idx].activespanel.split(",,")
            tmp4=prlist[idx].unactivespanel.split(",,")
            tmp7=prlist[idx].catorder.split(",,")
            tmp8=prlist[idx].activesnpanel.split(",,")
            tmp9=prlist[idx].unactivesnpanel.split(",,")
            for p in tmp1:
                activecatlist.append(p)
            for p in tmp2:
                unactivecatlist.append(p)
            for p in tmp3:
                activepanellist.append(p)
            for p in tmp4:
                unactivepanellist.append(p)
            for p in tmp7:
                catorderlist.append(p)
            for p in tmp8:
                activenpanelslist.append(p)
            for p in tmp9:
                unactivenpanelslist.append(p)
                    
            #get pinned cat and panels
            for p in plist:
                if p.keep_cat_hidden==True:
                    if p.panelstate==True:
                        pinactivecat.append(p.name)
                    else:
                        pinunactivecat.append(p.name)
            for p in nlist:
                if p.pin_npanel==True:
                    if p.n_panel_state==True:
                        pinactivenpanels.append(p.name)
                    else:
                        pinunactivenpanels.append(p.name)
                
            #delete prop lists
            if len(plist)>=1:
                for i in range(len(plist)-1,-1,-1):
                    plist.remove(i)
                    
            #Recreate cat list
            for p in catorderlist:
                if p!="":
                    chk=0
                    chk2=0
                    newcat=plist.add()
                    newcat.name=p
                    newcat.panelstate=True
                    for p2 in pinactivecat:
                        if p==p2:
                            chk=1
                    for p3 in pinunactivecat:
                        if p==p3:
                            chk2=1
                    if chk==0 and chk2==0:
                        for p4 in unactivecatlist:
                            if p==p4:
                                newcat.panelstate=False
                            newcat.keep_cat_hidden=False
                    elif chk==1 and chk2==0:
                        newcat.panelstate=True
                        newcat.keep_cat_hidden=True
                    elif chk==0 and chk2==1:
                        newcat.panelstate=False
                        newcat.keep_cat_hidden=True
        
            #apply active panel
            for p in slist:
                p.specific_panel_state=True
            for p in slist:
                for n in unactivecatlist:
                    if p.parent_category==n:
                        p.specific_panel_state=False
            for p in slist:
                for p2 in unactivepanellist:
                    if p2!="":
                        p4=p2.split("''")
                        if p.name==p4[0] and p.panel_context==p4[1] and p.panel_module==p4[2] and p.parent_category==p4[3]:
                            p.specific_panel_state=False
                                                
            #register exception for cat priority
            for e in slist:
                chk=0
                for n in pinactivecat:
                    if e.parent_category==n:
                        chk=1
                if chk==1:
                    e.specific_panel_state=True
                    
            #load specific panels details
            for p in slist2:
                for p2 in slist:
                    if p.name==p2.name:
                        if p.panel_context==p2.panel_context:
                            if p.panel_module==p2.panel_module:
                                p.specific_panel_state=p2.specific_panel_state
                                
            #set all N Panels unactive :
            for p in nlist:
                p.n_panel_state=False
            #activate good ones:
            for p in nlist:
                if p.name in activenpanelslist:
                    p.n_panel_state=True
            #reapply pined:
            for p in nlist:
                if p.name in pinactivenpanels:
                    p.n_panel_state=True
                elif p.name in pinunactivenpanels:
                    p.n_panel_state=False
                    
            bpy.ops.cathide.updatetemp()
            
            info = 'Preset Loaded'
            self.report({'INFO'}, info)
        
        else:
            info = 'Please select a Preset'
            self.report({'ERROR'}, info)
    
        return {'FINISHED'}

# Update temporary list
class CathideUpdateTemporary(bpy.types.Operator):
    bl_idname = "cathide.updatetemp"
    bl_label = "Update Temporary Panels List"
        
    def execute(self, context):
        scene=bpy.context.scene
        plist=scene.cathide_panel_list
        slist=scene.cathide_temporary_panel_list
        slist2=scene.cathide_specific_panel_list
        idx=scene.cathide_index
        contextsensitive=scene.cathide_show_onlycontext_specific
        
        #check selected category
        if (idx+1)<=len(plist):
            catok=plist[idx].name
        else:
            catok="No_Panel"
        
        #save to specific panel list
        for p in slist:
            for p2 in slist2:
                if p.name==p2.name:
                    if p.panel_context==p2.panel_context:
                        if p.panel_module==p2.panel_module:
                            p2.specific_panel_state=p.specific_panel_state
        #clear specific panel list
        for i in range(len(slist)-1,-1,-1):
            slist.remove(i)

        #find panels from current category and append them        
        if contextsensitive==True:
            for panel in bpy.types.Panel.__subclasses__():
                if hasattr(panel, 'bl_space_type'):
                    if hasattr(panel, 'bl_region_type'):
                        if hasattr(panel, 'bl_category'):
                            if hasattr(panel, 'bl_label'):
                                if panel.bl_space_type=="VIEW_3D":
                                    if panel.bl_region_type=="TOOLS":
                                        if panel.bl_category == catok:
                                            if hasattr(panel, 'bl_context'):
                                                pass
                                            else:
                                                if "poll" not in panel.__dict__:
                                                    if "bl_rna" in panel.__dict__:
                                                            newpan=slist.add()
                                                            newpan.name=panel.bl_label
                                                            newpan.specific_panel_state=True
                                                            newpan.panel_module=panel.__module__
                                                            if "bl_context" in panel.__dict__:
                                                                newpan.panel_context=panel.bl_context
                                                    elif "bl_rna" not in panel.__dict__:
                                                        newpan=slist.add()
                                                        newpan.name=panel.bl_label
                                                        newpan.specific_panel_state=False
                                                        newpan.panel_module=panel.__module__
                                                        if "bl_context" in panel.__dict__:
                                                            newpan.panel_context=panel.bl_context
                                                

        else:
            for panel in bpy.types.Panel.__subclasses__():
                if hasattr(panel, 'bl_space_type'):
                    if hasattr(panel, 'bl_region_type'):
                        if hasattr(panel, 'bl_category'):
                            if hasattr(panel, 'bl_label'):
                                if panel.bl_space_type=="VIEW_3D":
                                    if panel.bl_region_type=="TOOLS":
                                        if panel.bl_category == catok:
                                            if "bl_rna" in panel.__dict__:
                                                newpan=slist.add()
                                                newpan.name=panel.bl_label
                                                newpan.specific_panel_state=True
                                                newpan.panel_module=panel.__module__
                                                if "bl_context" in panel.__dict__:
                                                    newpan.panel_context=panel.bl_context
                                                elif "poll" in panel.__dict__:
                                                    newpan.panel_context="poll function"
                                            elif "bl_rna" not in panel.__dict__:
                                                newpan=slist.add()
                                                newpan.name=panel.bl_label
                                                newpan.specific_panel_state=False
                                                newpan.panel_module=panel.__module__
                                                if "bl_context" in panel.__dict__:
                                                    newpan.panel_context=panel.bl_context
                                                elif "poll" in panel.__dict__:
                                                    newpan.panel_context="poll function"
                                                    
        #load specific panels details
        for p in slist:
            for p2 in slist2:
                if p.name==p2.name:
                    if p.panel_context==p2.panel_context:
                        if p.panel_module==p2.panel_module:
                            p.specific_panel_state=p2.specific_panel_state
                    
        scene.cathide_specific_index=0
        
        return {'FINISHED'}

# Update NPanels nocontext list
class CathideUpdateNocontext(bpy.types.Operator):
    bl_idname = "cathide.updatenocontext"
    bl_label = "Update N-Panels No Context List"
        
    def execute(self, context):
        scene=bpy.context.scene
        nlist=scene.cathide_npanel_list
        nlistnc=scene.cathide_npanelnocontext_list
        contextsensitive=scene.cathide_show_onlycontext_npanels
        
        if contextsensitive==False:
            #save to specific panel list
            for p in nlistnc:
                for p2 in nlist:
                    if p.name==p2.name:
                        if p.n_panel_context==p2.n_panel_context:
                            if p.n_panel_module==p2.n_panel_module:
                                p2.n_panel_state=p.n_panel_state
                                p2.pin_npanel=p.pin_npanel
        elif contextsensitive==True:
            #save to specific panel list
            for p in nlist:
                for p2 in nlistnc:
                    if p.name==p2.name:
                        if p.n_panel_context==p2.n_panel_context:
                            if p.n_panel_module==p2.n_panel_module:
                                p2.n_panel_state=p.n_panel_state
                                p2.pin_npanel=p.pin_npanel
        
        scene.cathide_npanel_index=0
        
        return {'FINISHED'}

# Reset Cathide
class CathideReset(bpy.types.Operator):
    bl_idname = "cathide.reset"
    bl_label = "Reset Cathide"
    bl_description = "Reset Cathide Categories and Panels"
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
    
# Reset specific panels
class CathideResetSpecific(bpy.types.Operator):
    bl_idname = "cathide.reset_specific"
    bl_label = "Reset Cathide Specific Panels"
    bl_description = "Reset Cathide Specific Panels Only"
    bl_options = {'REGISTER', 'UNDO'}
        
    def execute(self, context):
        scene=bpy.context.scene
        plist=scene.cathide_panel_list
        slist=scene.cathide_specific_panel_list
        slist2=scene.cathide_temporary_panel_list
        idx=scene.cathide_index
        
        #save to specific panel list
        for p in slist2:
            for p2 in slist:
                if p.name==p2.name:
                    if p.panel_context==p2.panel_context:
                        if p.panel_module==p2.panel_module:
                            p2.specific_panel_state=p.specific_panel_state
        
        #check selected category
        if (idx+1)<=len(plist):
            catok=plist[idx].name
        else:
            catok="No_Panel"
                
        for p in slist:
            chk=0
            if p.parent_category==catok and p.specific_panel_state==False and (idx+1)<=len(plist):
                p2=plist[idx]
                if p2.panelstate==False and p2.keep_cat_hidden==True:
                    break
                else:
                    p.specific_panel_state=True
                    
        #load specific panels details
        for p in slist2:
            for p2 in slist:
                if p.name==p2.name:
                    if p.panel_context==p2.panel_context:
                        if p.panel_module==p2.panel_module:
                            p.specific_panel_state=p2.specific_panel_state
                
        bpy.ops.cathide.applyspecific()
        bpy.ops.cathide.updatetemp()
                    
        info = 'Specific Panels Reset'
        self.report({'INFO'}, info)
    
        return {'FINISHED'}
    
# Copy Preset to Scene
def cathidecopypresets(scn, self, context):
    scene=bpy.context.scene
    scenename=str(scene.name)
    plist=scene.cathide_preset_list
    idx=scene.cathide_preset_index
    copyall = bpy.context.scene.cathide_copyallpresets
    dt2 = datetime.datetime.today().strftime("%Y-%m-%d_%H:%M:%S")
    pcount=0
    
    for sc in bpy.data.scenes:
        if sc.name==scn:
            chk=0
            if copyall == True:
                for p in plist:
                    for po in sc.cathide_preset_list:
                        if po.name==p.name:
                            chk=1
                    new=sc.cathide_preset_list.add()
                    if chk==1:
                        new.name=p.name + " - " + str(dt2)
                    else:
                        new.name=p.name
                    new.activecat=p.activecat
                    new.unactivecat=p.unactivecat
                    new.unactivespanel=p.unactivespanel
                    new.activespanel=p.activespanel
                    new.catorder=p.catorder
                    pcount=pcount+1
                info = str(pcount) + ' CatHide Preset(s) copied to ' + str(sc.name)
                self.report({'INFO'}, info)
            else:
                if idx > len(plist):
                    info = 'Please select a CatHide Preset'
                    self.report({'ERROR'}, info)
                else:
                    chk=0
                    p=plist[idx]
                    for po in sc.cathide_preset_list:
                        if po.name==p.name:
                            chk=1
                    new=sc.cathide_preset_list.add()
                    if chk==1:
                        new.name=p.name + " - " +  str(dt2)
                    else:
                        new.name=p.name
                    new.activecat=p.activecat
                    new.unactivecat=p.unactivecat
                    new.unactivespanel=p.unactivespanel
                    new.activespanel=p.activespanel
                    new.catorder=p.catorder
                    info = 'CatHide Preset copied to ' + str(sc.name)
                    self.report({'INFO'}, info) 
                    
class CathideCopyPreset(bpy.types.Operator):
    bl_idname = "cathide.copypreset_toscene"
    bl_label = "Copy Cathide Preset(s)"
    bl_description = "Copy Cathide Preset(s) to other Scene"
    bl_options = {'REGISTER', 'UNDO'}
    scn = bpy.props.StringProperty()

    
    def execute(self, context):
        cathidecopypresets(self.scn, self, context)
        return {'FINISHED'}
        

        return {'FINISHED'}
    
# Menu Validation Clear All Presets
class CatHideDeleteAllPresetsMenu(bpy.types.Menu):
    bl_label = "Delete all CatHide Presets"
    bl_idname = "Menu_DeleteAll_CatHidePresets"
    
    def draw(self, context):
        layout = self.layout
        
        layout.operator("cathide.presetclear",text="Click to Clear All", icon='ERROR')

# Call Validation Clear All Presets Menu
def callclearpresetsmenu (context):
    bpy.ops.wm.call_menu(name=CatHideDeleteAllPresetsMenu.bl_idname)
    
class CatHideCallClearPresetsMenu(bpy.types.Operator):
    """Delete all CatHide Presets"""
    bl_idname = "call.clearpresets_menu"
    bl_label = "Call Clear All CatHide Presets Menu"

    def execute(self, context):
        callclearpresetsmenu(context)
        return {'FINISHED'}
    
# Menu Validation Update Presets
class CatHideUpdatePresetsMenu(bpy.types.Menu):
    bl_label = "Update Selected CatHide Presets"
    bl_idname = "Menu_Update_CatHidePreset"
    
    def draw(self, context):
        layout = self.layout
        idx = bpy.context.scene.cathide_preset_index
        selected = bpy.context.scene.cathide_preset_list[idx].name
        layout.operator("cathide.presetupdate",text="Click to Update - " + selected, icon='SETTINGS')
    
# Call Update Presets Menu
def callupdatepresetsmenu (context):
    bpy.ops.wm.call_menu(name=CatHideUpdatePresetsMenu.bl_idname)
    
class CatHideCallUpdatePresetsMenu(bpy.types.Operator):
    """Update Selected CatHide Preset"""
    bl_idname = "call.updatepresets_menu"
    bl_label = "Call Update Presets Menu"

    def execute(self, context):
        callupdatepresetsmenu(context)
        return {'FINISHED'} 
    
# Menu Copy presets to scene 
class CatHideCopyPresetsMenu(bpy.types.Menu):
    """Copy Preset to other Scene"""
    bl_label = "Copy Preset to Scene"
    bl_idname = "CatHide_CopyPreset_ToScene"
    
    def draw(self, context):
        layout = self.layout
        scenes=bpy.data.scenes
        Cscene=bpy.context.scene
        
        if len(scenes) > 1:
            for s in scenes:
                if s != Cscene:
                    s2=str(s.name)
                    opcopy=layout.operator('cathide.copypreset_toscene', text=s.name, icon='SCENE_DATA')
                    opcopy.scn = s2
        else:
            layout.label("Only One Scene in this blend file", icon='ERROR')  

# Create custom property group
class CatHidePanelList(bpy.types.PropertyGroup):
    '''name = StringProperty() '''
    panelstate = bpy.props.BoolProperty(name="panelstate", default = True)
    keep_cat_hidden = bpy.props.BoolProperty(name="keep_cat_hidden", description="PIN : If active, the state of the Category will not be reset by other Actions",default = False)

class CatHideTemporaryPanelList(bpy.types.PropertyGroup):
    '''name = StringProperty() '''
    specific_panel_state = bpy.props.BoolProperty(name="specific_panel_state", default = True)
    panel_context = bpy.props.StringProperty(name="panel_context")
    panel_module = bpy.props.StringProperty(name="panel_module")
        
class CatHideSpecificPanelList(bpy.types.PropertyGroup):
    '''name = StringProperty() '''
    parent_category = bpy.props.StringProperty(name="parent_category")
    specific_panel_state = bpy.props.BoolProperty(name="specific_panel_state", default = True)
    panel_context = bpy.props.StringProperty(name="panel_context")
    panel_module = bpy.props.StringProperty(name="panel_module")
    
class CatHideNPanelList(bpy.types.PropertyGroup):
    '''name = StringProperty() '''
    n_panel_state = bpy.props.BoolProperty(name="n_panel_state", default = True)
    n_panel_context = bpy.props.StringProperty(name="n_panel_context")
    n_panel_module = bpy.props.StringProperty(name="n_panel_module")
    pin_npanel = bpy.props.BoolProperty(name="pin_npanel", default = False)
    
class CatHideNPanelListNoContext(bpy.types.PropertyGroup):
    '''name = StringProperty() '''
    n_panel_state = bpy.props.BoolProperty(name="n_panel_state", default = True)
    n_panel_context = bpy.props.StringProperty(name="n_panel_context")
    n_panel_module = bpy.props.StringProperty(name="n_panel_module")
    pin_npanel = bpy.props.BoolProperty(name="pin_npanel", default = False)
    
class CatHidePresetList(bpy.types.PropertyGroup):
    '''name = StringProperty(default = "Cathide Preset")'''
    activecat = bpy.props.StringProperty(name="activecat")
    unactivecat = bpy.props.StringProperty(name="unactivecat")
    activespanel = bpy.props.StringProperty(name="activespanel")
    unactivespanel = bpy.props.StringProperty(name="unactivespanel")
    activesnpanel = bpy.props.StringProperty(name="activesnpanel")
    unactivesnpanel = bpy.props.StringProperty(name="unactivesnpanel")
    catorder = bpy.props.StringProperty(name="catorder")
    npanelsorder = bpy.props.StringProperty(name="npanelsorder")
        
# -------------------------------------------------------------------
# register
# -------------------------------------------------------------------

def register():
    bpy.utils.register_class(CatHideUIList)
    bpy.utils.register_class(CatHideSpecificUIList)
    bpy.utils.register_class(CatHideNUIList)
    bpy.utils.register_class(CatHidePresetUIList)
    bpy.utils.register_class(CatHideListActions)
    bpy.utils.register_class(CatHidePanel)
    bpy.utils.register_class(CathideRefresh)
    bpy.utils.register_class(CathideApply)
    bpy.utils.register_class(CathideApplyNPanels)
    bpy.utils.register_class(CathideApplySpecific)
    bpy.utils.register_class(CathidePresetAdd)
    bpy.utils.register_class(CathidePresetUpdate)
    bpy.utils.register_class(CathidePresetDelete)
    bpy.utils.register_class(CathidePresetClear)
    bpy.utils.register_class(CathideApplyPreset)
    bpy.utils.register_class(CathideLoadPreset)
    bpy.utils.register_class(CathideReset)
    bpy.utils.register_class(CathideResetSpecific)
    bpy.utils.register_class(CathideCopyPreset)
    bpy.utils.register_class(CathideUpdateTemporary)
    bpy.utils.register_class(CathideUpdateNocontext)
    bpy.utils.register_class(CatHideDeleteAllPresetsMenu)
    bpy.utils.register_class(CatHideCallClearPresetsMenu)
    bpy.utils.register_class(CatHideUpdatePresetsMenu)
    bpy.utils.register_class(CatHideCallUpdatePresetsMenu)
    bpy.utils.register_class(CatHideCopyPresetsMenu)
    bpy.utils.register_class(CatHidePanelList)
    bpy.types.Scene.cathide_panel_list = \
        bpy.props.CollectionProperty(type=CatHidePanelList)
    bpy.types.Scene.cathide_index = IntProperty(update=update_specificpanel_list)
    bpy.utils.register_class(CatHideTemporaryPanelList)
    bpy.types.Scene.cathide_temporary_panel_list = \
        bpy.props.CollectionProperty(type=CatHideTemporaryPanelList)
    bpy.utils.register_class(CatHideSpecificPanelList)
    bpy.types.Scene.cathide_specific_panel_list = \
        bpy.props.CollectionProperty(type=CatHideSpecificPanelList)
    bpy.types.Scene.cathide_specific_index = IntProperty()
    bpy.utils.register_class(CatHideNPanelList)
    bpy.types.Scene.cathide_npanel_list = \
        bpy.props.CollectionProperty(type=CatHideNPanelList)
    bpy.utils.register_class(CatHideNPanelListNoContext)
    bpy.types.Scene.cathide_npanelnocontext_list = \
        bpy.props.CollectionProperty(type=CatHideNPanelListNoContext)
    bpy.utils.register_class(CatHidePresetList)
    bpy.types.Scene.cathide_preset_list = \
        bpy.props.CollectionProperty(type=CatHidePresetList)
    bpy.types.Scene.cathide_preset_index = IntProperty()
    bpy.types.Scene.cathide_show_toolshelfcat = BoolProperty()
    bpy.types.Scene.cathide_show_specific = BoolProperty()
    bpy.types.Scene.cathide_show_specific_details = BoolProperty()
    bpy.types.Scene.cathide_show_npanel_details = BoolProperty()
    bpy.types.Scene.cathide_npanel_index = IntProperty()
    bpy.types.Scene.cathide_show_npanels = BoolProperty()
    bpy.types.Scene.cathide_show_preset = BoolProperty()
    bpy.types.Scene.cathide_show_presetcatdetails = BoolProperty()
    bpy.types.Scene.cathide_show_presetspaneldetails = BoolProperty()
    bpy.types.Scene.cathide_show_presetsnpaneldetails = BoolProperty()
    bpy.types.Scene.cathide_show_presetsutility = BoolProperty()
    bpy.types.Scene.cathide_copyallpresets = BoolProperty(description='If checked, all CatHide Presets will be copied to other Scene')
    bpy.types.Scene.cathide_show_onlycontext_specific = BoolProperty(description='Hide Context Sensitive items', update=update_specificpanel_list)
    bpy.types.Scene.cathide_show_onlycontext_npanels = BoolProperty(description='Hide Context Sensitive items', update=update_npanelnocontext_list)

def unregister():
    bpy.utils.unregister_class(CatHideUIList)
    bpy.utils.unregister_class(CatHideSpecificUIList)
    bpy.utils.unregister_class(CatHideNUIList)
    bpy.utils.unregister_class(CatHidePresetUIList)
    bpy.utils.unregister_class(CatHideListActions)
    bpy.utils.unregister_class(CatHidePanel)
    bpy.utils.unregister_class(CathideRefresh)
    bpy.utils.unregister_class(CathideApply)
    bpy.utils.unregister_class(CathideApplyNPanels)
    bpy.utils.unregister_class(CathideApplySpecific)
    bpy.utils.unregister_class(CathidePresetAdd)
    bpy.utils.unregister_class(CathidePresetUpdate)
    bpy.utils.unregister_class(CathidePresetDelete)
    bpy.utils.unregister_class(CathidePresetClear)
    bpy.utils.unregister_class(CathideApplyPreset)
    bpy.utils.unregister_class(CathideLoadPreset)
    bpy.utils.unregister_class(CathideUpdateTemporary)
    bpy.utils.unregister_class(CathideUpdateNocontext)
    bpy.utils.unregister_class(CathideReset)
    bpy.utils.unregister_class(CathideResetSpecific)
    bpy.utils.unregister_class(CathideCopyPreset)
    bpy.utils.unregister_class(CatHideDeleteAllPresetsMenu)
    bpy.utils.unregister_class(CatHideCallClearPresetsMenu)
    bpy.utils.unregister_class(CatHideUpdatePresetsMenu)
    bpy.utils.unregister_class(CatHideCallUpdatePresetsMenu)
    bpy.utils.unregister_class(CatHideCopyPresetsMenu)
    bpy.utils.unregister_class(CatHidePanelList)
    del bpy.types.Scene.cathide_panel_list
    bpy.utils.unregister_class(CatHideSpecificPanelList)
    del bpy.types.Scene.cathide_specific_panel_list
    bpy.utils.unregister_class(CatHideTemporaryPanelList)
    del bpy.types.Scene.cathide_temporary_panel_list
    bpy.utils.unregister_class(CatHideNPanelList)
    del bpy.types.Scene.cathide_npanel_list
    bpy.utils.unregister_class(CatHideNPanelListNoContext)
    del bpy.types.Scene.cathide_npanelnocontext_list
    bpy.utils.unregister_class(CatHidePresetList)
    del bpy.types.Scene.cathide_preset_list
    del bpy.types.Scene.cathide_index
    del bpy.types.Scene.cathide_specific_index
    del bpy.types.Scene.cathide_preset_index
    del bpy.types.Scene.cathide_show_toolshelfcat
    del bpy.types.Scene.cathide_show_specific
    del bpy.types.Scene.cathide_show_specific_details
    del bpy.types.Scene.cathide_show_npanel_details
    del bpy.types.Scene.cathide_npanel_index
    del bpy.types.Scene.cathide_show_npanels
    del bpy.types.Scene.cathide_show_preset
    del bpy.types.Scene.cathide_show_presetcatdetails
    del bpy.types.Scene.cathide_show_presetspaneldetails
    del bpy.types.Scene.cathide_show_presetsnpaneldetails
    del bpy.types.Scene.cathide_show_presetsutility
    del bpy.types.Scene.cathide_copyallpresets
    del bpy.types.Scene.cathide_show_onlycontext_specific
    del bpy.types.Scene.cathide_show_onlycontext_npanels
    
if __name__ == "__main__":
    register()
