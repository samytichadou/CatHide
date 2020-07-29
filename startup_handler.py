import bpy
from bpy.app.handlers import persistent

### HANDLER ###
@persistent
def cathideStartupHandler(scene):
    
    print("CatHide") #debug