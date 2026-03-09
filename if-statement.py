# implement if-statement in Blender
# creating random shapes

import bpy

# extend to generate random numbers 
import random 

# initialize
current_location = 0

# creating 10
for i in range (10):
    current_location = current_location + 2 
    if random.randint (0,1):
        bpy.ops.mesh.primitive_ico_sphere_add(location = (current_location,0,current_location))
    else: 
        bpy.ops.mesh.primitive_cube_add(location = (current_location,0,current_location))




