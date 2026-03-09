import random
import time # "random seed"
import math

import bpy
# math model creation 
import mathutils

# resource: how to clean scene:
# https://youtu.be/3rNqVPtbhzc?si=cfgoQc4R7PFI1e2F 

# recursion function to clean 
def purge_orphans(): # data based 
    # remove 
        result = bpy.ops.outliner.orphans_purge()
        if result.pop() != "CANCELLED":
            purge_orphans() # run until nothing can be cancelled
            

# ensure everytime refresh，new objects 
def clean_scene():
    # in Edit Mode
    if bpy.context.active_object and bpy.context.active_object.mode == "EDIT":
        bpy.ops.object.editmode_toggle()
        
    # no objects are hidden 
    for obj in bpy.data.objects:
        obj.hide_set(False)
        obj.hide_select = False
        obj.hide_viewport = False

    # select all the object and delete them
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()

    # all collections and remove them
    collection_names = [col.name for col in bpy.data.collections]
    for name in collection_names:
        bpy.data.collections.remove(bpy.data.collections[name])

    #  recreate the world object
    world_names = [world.name for world in bpy.data.worlds]
    for name in world_names:
        bpy.data.worlds.remove(bpy.data.worlds[name])
        
    # create a new world data （data is the most important part！！！）
    bpy.ops.world.new()
    bpy.context.scene.world = bpy.data.worlds["World"]

    purge_orphans()


def active_object():
    
    return bpy.context.active_object


def time_seed():

    seed = time.time()
    print(f"seed: {seed}")
    random.seed(seed)

    # add the seed value to clipboard so that can be used repeatedly 
    bpy.context.window_manager.clipboard = str(seed)

    return seed


def setup_camera():
    # fail to build functions 
    # copy all instructions 
    bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=(0, 0, 0), rotation=(1.5708, -0, 1.5708))
    bpy.ops.transform.translate(value=(1.08539e-15, 2.41005e-31, 4.88817), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
    bpy.ops.transform.rotate(value=1.57027, orient_axis='Z', orient_type='VIEW', orient_matrix=((1, 0, 0), (0, -1.34359e-07, -1), (0, -1, -1.34359e-07)), orient_matrix_type='VIEW', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
    bpy.ops.transform.translate(value=(0, 3.18005e-07, 2.36683), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
    bpy.ops.transform.translate(value=(7.04241e-16, 0.194181, 3.17162), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)


def set_1080px_square_render_res():

    bpy.context.scene.render.resolution_x = 1080
    bpy.context.scene.render.resolution_y = 1080


def set_scene_props(fps, loop_seconds):

    """
    scene properties for an EEVEE animation loop

    Args:
    fps (int): Frames per second for the animation.
    loop_seconds (float): Duration of the loop in seconds
    """

    frame_count = fps * loop_seconds

    scene = bpy.context.scene
    scene.frame_end = frame_count

    # set the world background to black
    world = bpy.data.worlds["World"]
    if "Background" in world.node_tree.nodes:
        world.node_tree.nodes["Background"].inputs[0].default_value = (0, 0, 0, 1)

    scene.render.fps = fps

    scene.frame_current = 1
    scene.frame_start = 1
    
    # how to set up eevve rendering 
    # resource: https://youtu.be/j96Ddru2hdQ?si=vYsMDzCDICub5SOH
    scene.eevee.use_bloom = True
    scene.eevee.bloom_intensity = 0.005

    # set Ambient Occlusion properties
    scene.eevee.use_gtao = True
    scene.eevee.gtao_distance = 4
    scene.eevee.gtao_factor = 5

    scene.eevee.taa_render_samples = 64

    scene.view_settings.look = "Very High Contrast"

    set_1080px_square_render_res()


def setup_scene():
    fps = 30
    loop_seconds = 12
    frame_count = fps * loop_seconds

    seed = 0
    if seed:
        random.seed(seed)
    else:
        time_seed()

    # Building Blocks
    clean_scene()
    set_scene_props(fps, loop_seconds)

    loc = (0, 0, 7)
    rot = (0, 0, 0)
    setup_camera()

    context = {
        "frame_count": frame_count,
    }

    return context


def make_fcurves_linear():
    # linear action 
    for fc in bpy.context.active_object.animation_data.action.fcurves:
        fc.extrapolation = "LINEAR"


def get_random_color():
    return random.choice(
        [
            [0.92578125, 1, 0.0, 1],
            [0.203125, 0.19140625, 0.28125, 1],
            [0.8359375, 0.92578125, 0.08984375, 1],
            [0.16796875, 0.6796875, 0.3984375, 1],
            [0.6875, 0.71875, 0.703125, 1],
            [0.9609375, 0.9140625, 0.48046875, 1],
            [0.79296875, 0.8046875, 0.56640625, 1],
            [0.96484375, 0.8046875, 0.83984375, 1],
            [0.91015625, 0.359375, 0.125, 1],
            [0.984375, 0.4609375, 0.4140625, 1],
            [0.0625, 0.09375, 0.125, 1],
            [0.2578125, 0.9140625, 0.86328125, 1],
            [0.97265625, 0.21875, 0.1328125, 1],
            [0.87109375, 0.39453125, 0.53515625, 1],
            [0.8359375, 0.92578125, 0.08984375, 1],
            [0.37109375, 0.29296875, 0.54296875, 1],
            [0.984375, 0.4609375, 0.4140625, 1],
            [0.92578125, 0.16796875, 0.19921875, 1],
            [0.9375, 0.9609375, 0.96484375, 1],
            [0.3359375, 0.45703125, 0.4453125, 1],
        ]
    )


def render_loop():
    bpy.ops.render.render(animation=True)


def apply_random_color_material(obj):
    """
    Creates and applies a randomly colored material to an object

    Args:
    obj (bpy.types.Object): The Blender mesh object to apply the material to.
    """

    color = get_random_color()
    mat = bpy.data.materials.new(name="Material")
    mat.use_nodes = True
    mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = color

    mat.node_tree.nodes["Principled BSDF"].inputs["Specular"].default_value = 0
   
    obj.data.materials.append(mat) # give material to objects 


def add_lights():
    # fail to build functions
    # copy all the hand instructions
    rotation = (math.radians(60), 0.0, math.radians(180))
    bpy.ops.object.light_add(type="SUN", rotation=rotation)
    bpy.context.object.data.energy = 2
    bpy.context.object.data.angle = math.radians(45)
    bpy.ops.transform.translate(value=(-2.19608, 13.4895, 2.56032), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
    bpy.ops.transform.translate(value=(9.28085e-16, -1.51074, 4.17972), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
    bpy.ops.transform.translate(value=(-2.10749, -12.6644, 2.09707), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
    bpy.ops.transform.rotate(value=-1.14124, orient_axis='Z', orient_type='VIEW', orient_matrix=((-0.282297, -0.959327, -1.41561e-07), (0.208774, -0.0614347, -0.976032), (-0.936335, 0.275531, -0.217625)), orient_matrix_type='VIEW', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
    bpy.ops.transform.translate(value=(4.20725, 1.0436e-07, 0.776723), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
    bpy.ops.transform.rotate(value=-0.368472, orient_axis='Z', orient_type='VIEW', orient_matrix=((1, 0, -0), (0, -1.34359e-07, -1), (0, -1, -1.34359e-07)), orient_matrix_type='VIEW', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)


# set up key frames
def loop_param(obj, param_name, start_value, mid_value, frame_count):
    """
    Animates an object property in a ping-pong loop: start → mid → start

    Args:
    obj: The Blender object whose property will be animated.
    param_name (str): The name to animate
    start_value: The value at frame 1 
    mid_value: The value at the halfway 
    frame_count (int): Total number of frames in the animation loop.
    """
    
    frame = 1

    setattr(obj, param_name, start_value)
    obj.keyframe_insert(param_name, frame=frame)

    frame = frame_count / 2
    setattr(obj, param_name, mid_value)
    obj.keyframe_insert(param_name, frame=frame)

    frame = frame_count
    setattr(obj, param_name, start_value)
    obj.keyframe_insert(param_name, frame=frame)


def set_keyframe_to_ease_in_out(obj):
    """
    Sets all keyframes on an object's action to BACK / EASE_IN_OUT 

    Args:
    obj (bpy.types.Object): The animated Blender object to update.
    """

    for fcurve in obj.animation_data.action.fcurves:
        for kf in fcurve.keyframe_points:
            # easing animation "back" to make shapes move more smooth
            kf.interpolation = "BACK"
            kf.easing = "EASE_IN_OUT"


def animate_shape(obj, vertices, start_frame, end_frame):
    """
    Animates a shape with a two-turn Z rotation using ease-in-out 

    Args:
    obj (bpy.types.Object): The Blender object to animate
    vertices (int): Number of vertices of the shape
    start_frame (int): Frame at which the rotation begins
    end_frame (int): Frame at which the rotation ends
    """
    obj.keyframe_insert("rotation_euler", frame=start_frame)

    one_turn = 360 / vertices
    # turn two rounds 
    obj.rotation_euler.z += math.radians(one_turn * 2)

    obj.keyframe_insert("rotation_euler", frame=end_frame)

    # inactive
    set_keyframe_to_ease_in_out(obj)


def create_shape(vertices, radius, rotation, location):
    """
    Creates a (polygon) mesh with a random color material.

    Args:
    vertices (int): Number of vertices(sides) for the polygon.
    radius (float): Radius of the cylinder.
    rotation (mathutils.Euler): XYZ Euler rotation to apply to the object.
    location (mathutils.Vector): XYZ world-space location for the object.
    """

    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=0.1)

    obj = active_object()
    obj.rotation_euler = rotation
    obj.location = location

    apply_random_color_material(obj)

    bpy.ops.object.modifier_add(type="BEVEL")
    # add modifier to adjust the shape
    obj.modifiers["Bevel"].width = 0.02

    return obj


def gen_centerpiece(context):
    """
    Generates the main animated piece

    Args:
    context (dict): scene context
    """
    
    # increase by 1 by layers 
    radius_step = 0.1
    radius = 1

    vertices = 5

    shape_count = 100
    
    # every layer move down "0.1"
    z_location_step = -0.1
    current_location = mathutils.Vector((0, 0, 0))
    
    # rotate 
    z_rotation_step = math.radians(5)
    current_rotation = mathutils.Euler((0.0, 0.0, 0.0))
    
    # wait for 5 frames for every layer
    start_frame_step = 5
    end_frame = context["frame_count"] - 10

    for i in range(shape_count):
        start_frame = start_frame_step * i

        current_rotation.z = z_rotation_step * i
        current_location.z = z_location_step * i

        shape_obj = create_shape(vertices, radius, current_rotation, current_location)
        animate_shape(shape_obj, vertices, start_frame, end_frame)
        
        # increating radius 
        radius += radius_step


def main():

    context = setup_scene()
    gen_centerpiece(context) # main animation 
    add_lights() 


if __name__ == "__main__":
    main()