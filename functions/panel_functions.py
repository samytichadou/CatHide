import bpy

# get all panel for space_type
def getAllPanelFromSpaceRegion(space_type, region_type):
    
    panel_list = []
    
    category_list = []
    
    panel_child_list = []
    
    for panel in bpy.types.Panel.__subclasses__():
        
        if hasattr(panel, 'bl_space_type') and hasattr(panel, 'bl_region_type'):
            
            if panel.bl_space_type == space_type and panel.bl_region_type == region_type:
                
                if hasattr(panel, 'bl_parent_id'):
                    
                    panel_child_list.append(panel)
                    
                else:
                
                    panel_list.append(panel)
                
                if panel.bl_category not in category_list:
                    
                    category_list.append(panel.bl_category)
                    
    return panel_list, category_list, panel_child_list


# create categories
def createPanelCategoriesProperties():
    
    panels, categories, child_panels = getAllPanelFromSpaceRegion("VIEW_3D", "UI")
    
    for cat in categories:
        
        print() #debug
        print(cat) #debug

        # TODO create category prop
        
        for panel in panels:
            
            if panel.bl_category == cat:
                
                print("|--" + panel.bl_label) #debug
                
                # TODO append panel in specified cat (label, context, id, original category)
                
                for child in child_panels:
                    
                    if child.bl_parent_id == panel.__name__:
                    
                        print("|--|--" + child.bl_label) #debug
                        
                        # TODO append child panel in specified panel (label, context, id, original category)


# get panel with ID
def getPanelWithId(id):
    
    panel = getattr(bpy.types, id)
    
    return Panel

                
# unregister panel
def unregisterPanel(panel):
    
    # check if registered
    if "bl_rna" in panel.__dict__:
        
        bpy.utils.unregister_class(panel)
        
        print("UNREG : " + panel) #debug
        # TODO set its property to hidden
        

# register panel
def registerPanel(panel):
    
    # check if registered
    if "bl_rna" not in panel.__dict__:
        
        bpy.utils.register_class(panel)
        
        print("REG : " + panel) #debug
        # TODO set its property to not hidden