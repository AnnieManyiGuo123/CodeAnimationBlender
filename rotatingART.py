import bpy

import math

import random 

def create_mesh():
    # add a cube mesh 
    bpy.ops.mesh.primitive_cube_add()

    # get a reference 
    obj = bpy.context.active_object

    # scale the cube mesh
    obj.scale.x *= 0.5
    obj.scale.y *= 2
    obj.scale.z *= 0.1

    # apply random rotation
    random_rotation = random.uniform(0, 360)
    obj.rotation_euler.z = math.radians(random_rotation)

    # apply the scale
    bpy.ops.object.transform_apply()

    return obj


def update_obj_transform(obj, current_angle):
    """
    Stacks an object directly on top of the previous layer & sets z rotation 

    Args:
    obj (bpy.types.Object): The Blender object to reposition and rotate.
    current_angle (float): The desired Z rotation 
    """

    # update the location 
    # demention: no space between stacks 
    obj.location.z += obj.dimensions.z

    # update the rotation
    obj.rotation_euler.z = math.radians(current_angle)


def animate_rotation(obj, current_frame, rotation_frame_count, clockwise):
    """
    Animates a full 360° rotation on the z axis through a set number of frames.

    Args:
    obj (bpy.types.Object): The Blender object to animate
    current_frame (int): The frame at which the rotation starts
    rotation_frame_count (int): Number of frames the rotation spans
    clockwise (bool): If True, rotates clockwise; otherwise counter-clockwise
    """

    # remove the animation data from the duplicated objects
    obj.animation_data_clear()

    # insert key frame
    obj.keyframe_insert("rotation_euler", frame=current_frame)

    # rotate object (two directions)
    if clockwise:
        angle = -360
    else:
        angle = 360
        
    obj.rotation_euler.z += math.radians(angle)

    # calculate the end frame
    frame = current_frame + rotation_frame_count

    # insert key frame (end)
    obj.keyframe_insert("rotation_euler", frame=frame)
    


def create_next_layer(current_angle, current_frame, rotation_frame_count, clockwise):
    """
    Duplicates the active mesh, positions it as the next layer, and then animates it.

    Args:
    current_angle (float): z rotation in degrees for the new layer
    current_frame (int): The frame at which the layer's rotation animation starts
    rotation_frame_count (int): Number of frames the rotation spans
    clockwise (bool): Rotation direction passed to animate_rotation() [checking]
    """

    # duplicate the mesh
    bpy.ops.object.duplicate(linked=True)

    # get a reference t
    obj = bpy.context.active_object

    update_obj_transform(obj, current_angle)

    animate_rotation(obj, current_frame, rotation_frame_count, clockwise)


def main():
    obj = create_mesh()

    # create variables for stacking and rotating
    angle_step = 3
    current_angle = angle_step

    # create variables for animating the rotation
    current_frame = 1
    frame_step = 1
    rotation_frame_count = 90
    
    # animated original 
    clockwise = True
    animate_rotation(obj, current_frame, rotation_frame_count, clockwise)

    # stack and rotate the mesh
    while current_angle <= 360:
        
        clockwise = not clockwise
        create_next_layer(current_angle, current_frame, rotation_frame_count, clockwise)

        # update the angle for the next iteration
        current_angle += angle_step

        # update the current_frame
        current_frame += frame_step

    # update the end frame for the whole animation
    bpy.context.scene.frame_end = current_frame + rotation_frame_count


main()