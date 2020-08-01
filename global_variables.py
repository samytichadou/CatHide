panels_exceptions = [
    "VIEW3D_PT_context_properties",     # builtin panel not from script, has to be registered
    ]


categories_exceptions = [
    "Item",     # builtin panel transform has to be registered
    ]


context_naming_list = [

    ["OBJECT", ".objectmode"],

    ["EDIT_MESH",".mesh_edit"],

    ["PAINT_TEXTURE",".imagepaint"],
    ["PAINT_WEIGHT",".weightpaint"],
    ["PAINT_VERTEX",".vertexpaint"],

    ["PAINT",".paint_common"], # common to all paint modes

    ["SCULPT",".sculpt_mode"],

    ["PARTICLE",".particlemode"],

    ["POSE",".posemode"],
    ["EDIT_ARMATURE",".armature_edit"],

    ["VERTEX_GPENCIL",".greasepencil_vertex"],
    ["EDIT_GPENCIL",".greasepencil_edit"],
    ["PAINT_GPENCIL",".greasepencil_paint"],
    ["SCULPT_GPENCIL",".greasepencil_sculpt"],
    ["WEIGHT_GPENCIL",".greasepencil_weight"],

    ["EDIT_CURVE",".curve_edit"],

    ]