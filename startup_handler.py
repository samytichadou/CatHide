import bpy
from bpy.app.handlers import persistent

from .functions.panel_functions import createPanelCategoriesProperties
from .global_variables import cathide_print

### HANDLER ###
@persistent
def cathideStartupHandler(scene):
    
    print(cathide_print + "Loading panels")

    createPanelCategoriesProperties()