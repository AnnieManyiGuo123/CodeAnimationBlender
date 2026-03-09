# make a cube from a list of vertices [list, tuples]

import bpy

# manipulating data and define

verts = [
    (-1.0, -1.0, -1.0), # 0
    (-1.0, 1.0, -1.0), # 1
    (1.0, 1.0, -1.0), # 2
    (1.0, -1.0, -1.0),
    (-1.0, -1.0, 1.0),
    (-1.0, 1.0, 1.0),
    (1.0, 1.0, 1.0),
    (1.0, -1.0, 1.0),
]

# lable the verts by numbers, creating faces
faces = [
    (0, 1, 2, 3),
    (7, 6, 5, 4),
    (4, 5, 1, 0),
    (7, 4, 0, 3),
    (6, 7, 3, 2),
    (5, 6, 2, 1),
]

edges = []

# create (store) data 
mesh_data = bpy.data.meshes.new("cube_data")
# use variabls e to populate 
mesh_data.from_pydata(verts, edges, faces)

# attach data to this object
mesh_obj = bpy.data.objects.new("cube_object", mesh_data)

# add object to the collection (appear)
bpy.context.collection.objects.link(mesh_obj)