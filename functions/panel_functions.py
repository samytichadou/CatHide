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

    winman = bpy.data.window_managers[0]

    viewport_panels_categories = winman.cathide_viewport_panels_categories
    
    panels, categories, child_panels = getAllPanelFromSpaceRegion("VIEW_3D", "UI")
    
    for cat in categories:
        
        print() #debug
        print(cat) #debug

        cat_entry = viewport_panels_categories.add()
        cat_entry.name = cat

        viewport_panels_panels = cat_entry.panels
        
        for panel in panels:
            
            if panel.bl_category == cat:
                
                print("|--" + panel.bl_label) #debug
                
                panel_entry = viewport_panels_panels.add()
                panel_entry.name = panel.bl_label
                panel_entry.idname = panel.__name__
                panel_entry.idtest = str(panel)
                panel_entry.original_category = cat
                if hasattr(panel, 'bl_context'):
                    panel_entry.context = panel.bl_context

                viewport_panels_childs = panel_entry.child_panels
                
                for child in child_panels:
                    
                    if child.bl_parent_id == panel.__name__:
                    
                        print("|--|--" + child.bl_label) #debug
                        
                        child_entry = viewport_panels_childs.add()
                        child_entry.name = child.bl_label
                        child_entry.idname = child.__name__
                        child_entry.original_category = cat
                        if hasattr(child, 'bl_context'):
                            child_entry.context = child.bl_context


# get panel with ID
def getPanelWithId(id):
    
    panel = getattr(bpy.types, id)
    
    return panel

                
# unregister panel
def unregisterPanel(panel):
    
    # check if registered
    if panel.is_registered:
        
        bpy.utils.unregister_class(panel)
        
        print("UNREG : " + panel.__name__) #debug
        # TODO set its property to hidden
        

# register panel
def registerPanel(panel):
    
    # check if registered
    if not panel.is_registered:
        
        bpy.utils.register_class(panel)
        
        print("REG : " + panel.__name__) #debug
        # TODO set its property to not hidden