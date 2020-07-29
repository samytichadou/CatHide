import bpy


class CatHide3DPanelsChilds(bpy.types.PropertyGroup) :
    '''name : StringProperty() '''
    id : bpy.props.StringProperty(name="ID")
    context : bpy.props.StringProperty(name="Context")
    original_category : bpy.props.StringProperty(name="Original Category")


class CatHide3DPanelsPanels(bpy.types.PropertyGroup) :
    '''name : StringProperty() '''
    id : bpy.props.StringProperty(name="ID")
    context : bpy.props.StringProperty(name="Context")
    original_category : bpy.props.StringProperty(name="Original Category")
    child_panels : bpy.props.CollectionProperty(type = CatHide3DPanelsChilds, name="Childs")


class CatHide3DPanelsCategories(bpy.types.PropertyGroup) :
    '''name : StringProperty() '''
    panels : bpy.props.CollectionProperty(type = CatHide3DPanelsPanels, name="Panels")