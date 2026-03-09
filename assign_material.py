# assigning materials/colors/textures to the object

import bpy
import random 
# access to Blender's mesh editing (data access)
import bmesh

# add an ico sphere
bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=3)
ico_object = bpy.context.active_object

# turn on eidt mode
bpy.ops.object.editmode_toggle()

# deselect all faces
bpy.ops.mesh.select_all()

# get data from object
ico_bmesh = bmesh.from_edit_mesh(ico_object.data)

# iterate through each face of the mesh
for face in ico_bmesh.faces:

    # generate a random color
    # creates a value from 0.0 to 1.0
    red = random.random()  
    green = random.random()
    blue = random.random()
    alpha = 1.0
    color = (red, green, blue, alpha)

    # keep creating new materials
    mat = bpy.data.materials.new(name=f"face_{face.index}")
    mat.diffuse_color = color

    # add the material to the object
    ico_object.data.materials.append(mat)

    # active material
    ico_object.active_material_index = face.index

    # select the face and assign 
    face.select = True
    bpy.ops.object.material_slot_assign()
    face.select = False

# turn off edit mode
bpy.ops.object.editmode_toggle()
