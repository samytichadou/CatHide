'''
Copyright (C) 2018 Samy Tichadou (tonton)
samytichadou@gmail.com

Created by Samy Tichadou (tonton)

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

bl_info = {  
 "name": "CatHide",  
 "author": "Samy Tichadou (tonton)",  
 "version": (2, 0),  
 "blender": (2, 90, 0), 
 "location": "3D View",  
 "description": "",  
 "wiki_url": "https://github.com/samytichadou/CatHide/",  
 "tracker_url": "https://github.com/samytichadou/CatHide/issues/new",  
 "category": "Interface",
 "warning": "Alpha version, use at your own risks"
 }


import bpy


# IMPORT SPECIFICS
##################################

from .startup_handler import cathideStartupHandler

from .properties import *

from .gui import *

from .operator.toggle_category_visibility import *

from .operator.move_panel_to_category import *

from .operator.refresh_lists_operator import *


# register
##################################

classes = (CatHideViewportPanelsChilds,
            CatHideViewportPanelsPanels,
            CatHideViewportPanelsCategories,

            CATHIDE_PT_panel,
            CATHIDE_UL_panel_ui_list,
            
            CATHIDE_OT_toggle_category_visibility,
            CATHIDE_OT_move_panel_to_category,
            CATHIDE_OT_refresh_lists,
            )

def register():

    ### OPERATORS ###
    from bpy.utils import register_class
    for cls in classes :
        register_class(cls)

    ### PROPERTIES ###
    bpy.types.WindowManager.cathide_viewport_panels_categories = \
        bpy.props.CollectionProperty(type = CatHideViewportPanelsCategories, name="CatHide 3D Panels Categories")

    ### HANDLER ###
    bpy.app.handlers.load_post.append(cathideStartupHandler)

    ### MENU ###
    bpy.types.VIEW3D_MT_editor_menus.append(topbar_menu_function)

    # init lists if needed TODO


def unregister():
    
    ### OPERATORS ###
    from bpy.utils import unregister_class
    for cls in reversed(classes) :
        unregister_class(cls)

    ### PROPERTIES ###
    del bpy.types.WindowManager.cathide_viewport_panels_categories

    ### HANDLER ###
    bpy.app.handlers.load_post.remove(cathideStartupHandler)

    ### MENU ###
    bpy.types.VIEW3D_MT_editor_menus.remove(topbar_menu_function)