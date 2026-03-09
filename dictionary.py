# apply dictionary in Blender
# concept: key-value

import bpy
import random 

cube_key = "cubes"
ico_key = "spheres"
cone_key = "cones"

# add ico spheres into the scene
object_count = 10

for _ in range(object_count):
    x = random.uniform(-5, 5)
    y = random.uniform(-5, 5)
    z = random.uniform(-5, 5)
    bpy.ops.mesh.primitive_ico_sphere_add(radius=1, location=(x, y, z))

# add cubes into the scene
for _ in range(object_count):
    x = random.uniform(-5, 5)
    y = random.uniform(-5, 5)
    z = random.uniform(-5, 5)
    bpy.ops.mesh.primitive_cube_add(location=(x, y, z))

# add cones into the scene
for _ in range(object_count):
    x = random.uniform(-5, 5)
    y = random.uniform(-5, 5)
    z = random.uniform(-5, 5)
    bpy.ops.mesh.primitive_cone_add(location=(x, y, z))

# create a dict of mesh lists
mesh_objects = {
    cube_key: list(),
    ico_key: list(),
    cone_key: list(),
}

# adding all meshs into the dict
for obj in bpy.data.objects:
    if "Cube" in obj.name:
        mesh_objects[cube_key].append(obj)
        continue

    if "Ico" in obj.name:
        mesh_objects[ico_key].append(obj)
        continue

    if "Cone" in obj.name:
        mesh_objects[cone_key].append(obj)

# create a dict of locations
mesh_z_locations = {
    cube_key: 0,
    ico_key: -5,
    cone_key: 5,
}

# loop over 
for key, value in mesh_objects.items():
    for mesh_obj in value:
        mesh_obj.location.z = mesh_z_locations[key]