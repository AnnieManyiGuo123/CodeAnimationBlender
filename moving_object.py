# moving a cube 

# give Python access to Blender's functionally
# import extension 
import bpy 

# add a cube into the scene
bpy.ops.mesh.primitive_cube_add()
# size=2, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1)

# get a reference to the currently active object
# in order to modify cube's location 
cube = bpy.context.active_object #(naming variable)
# Ex. changing name: cube.name = 'my cube'

# insert keyframe at frame one
# cube.location 
# Ex. setting location: cube.location.z = 4
# press TAB for parameter infor
start_frame = 1
cube.keyframe_insert("location", frame = start_frame)
# change the location of the cube 
cube.location.z = 5

# insert keyframe at the mid frame
mid_frame = 90
cube.keyframe_insert("location", frame = mid_frame)
# change the location
cube.location.z = 0

# insert keyframe at the last frame 
last_frame = 180
cube.keyframe_insert("location", frame = last_frame)
