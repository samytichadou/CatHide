import bpy


class CatHideViewportPanelsChilds(bpy.types.PropertyGroup) :
    '''name : StringProperty() '''
    idname : bpy.props.StringProperty(name="ID")
    context : bpy.props.StringProperty(name="Context")
    original_category : bpy.props.StringProperty(name="Original Category")


class CatHideViewportPanelsPanels(bpy.types.PropertyGroup) :
    '''name : StringProperty() '''
    idname : bpy.props.StringProperty(name="ID")
    context : bpy.props.StringProperty(name="Context")
    original_category : bpy.props.StringProperty(name="Original Category")
    child_panels : bpy.props.CollectionProperty(type = CatHideViewportPanelsChilds, name="Childs")


class CatHideViewportPanelsCategories(bpy.types.PropertyGroup) :
    '''name : StringProperty() '''
    panels : bpy.props.CollectionProperty(type = CatHideViewportPanelsPanels, name="Panels")