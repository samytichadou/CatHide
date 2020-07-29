import bpy
from bpy.app.handlers import persistent

from .functions.panel_functions import createPanelCategoriesProperties

### HANDLER ###
@persistent
def cathideStartupHandler(scene):
    
    print("CatHide loading panels : ") #debug

    createPanelCategoriesProperties()