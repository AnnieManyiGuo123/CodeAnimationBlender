# rotate a cube

import bpy
import math 

# add a cube # initial location
bpy.ops.mesh.primitive_cube_add()

# get a reference
cube = bpy.context.active_object

# first frame
start_frame = 1
cube.keyframe_insert("rotation_euler", frame = start_frame)


# change the rotation of the cube
# convert degrees into radians:
degree = 360
radians = math.radians(degree)
cube.rotation_euler.z = radians

degree = 360*2
radians = math.radians(degree)
cube.rotation_euler.x = radians

# last frame
end_frame = 180
cube.keyframe_insert("rotation_euler", frame = end_frame)