import bpy


class CatHideViewportPanelsChilds(bpy.types.PropertyGroup) :
    '''name : StringProperty() '''
    idname : bpy.props.StringProperty(name="ID")
    context : bpy.props.StringProperty(name="Context")
    # original_category : bpy.props.StringProperty(name="Original Category")
    hide : bpy.props.BoolProperty(name = "Hide")
    # display : bpy.props.BoolProperty(name = "Display Panel")

class CatHideViewportPanelsPanels(bpy.types.PropertyGroup) :
    '''name : StringProperty() '''
    idname : bpy.props.StringProperty(name="ID")
    context : bpy.props.StringProperty(name="Context")
    original_category : bpy.props.StringProperty(name="Original Category")
    hide : bpy.props.BoolProperty(name = "Hide")
    child_panels : bpy.props.CollectionProperty(type = CatHideViewportPanelsChilds, name="Childs")
    protected : bpy.props.BoolProperty()
    # display : bpy.props.BoolProperty(name = "Display Panel")
    # child_display : bpy.props.BoolProperty(name = "Display Childs")

class CatHideViewportPanelsCategories(bpy.types.PropertyGroup) :
    '''name : StringProperty() '''
    panels : bpy.props.CollectionProperty(type = CatHideViewportPanelsPanels, name="Panels")
    hide : bpy.props.BoolProperty(name = "Hide")
    display : bpy.props.BoolProperty(name = "Display Category")
    panels_display : bpy.props.BoolProperty(name = "Display Panels Informations")
    panels_index : bpy.props.IntProperty(min=-1)
    protected : bpy.props.BoolProperty()
    # show_all_panels : bpy.props.BoolProperty(name = "Show All Panels")