# creating triangles with different radius by using for-loop
import bpy 
import math 

# create variables used in the for loop
# initialize 
radius_step = 0.1
current_radius = 0.1
number_triangles = 50

z_step = 10

# repeat 50 times
for i in range (number_triangles):
    
    # add a triangle meth into the scene
    current_radius = current_radius + radius_step
    bpy.ops.mesh.primitive_circle_add (vertices = 3, radius = current_radius)

    # get a reference to the object
    triangle_mesh = bpy.context.active_object

    # rotate mesh about the x-axis; to radians
    degree = -90
    radians = math.radians(degree)
    triangle_mesh.rotation_euler.x = radians

    # rotate mesh about the z-axis; to radians
    degree = z_step*i
    radians = math.radians(degree)
    triangle_mesh.rotation_euler.z = radians

    # covert mesh into curve
    bpy.ops.object.convert(target='CURVE')

    # add bevel to curve
    # you can directly do it in Blender and then copy the order code
    triangle_mesh.data.bevel_depth = 0.05
    triangle_mesh.data.bevel_resolution = 16

    # shade smooth
    bpy.ops.object.shade_smooth()
