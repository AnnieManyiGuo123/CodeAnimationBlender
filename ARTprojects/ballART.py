import random
import time
import math

import bpy

#---------------initialize the scene-----------------------

# resource: https://youtu.be/3rNqVPtbhzc?si=51nrtldP6xwDcsj6 

def purge_orphans():
    # call recursively to remove all data and objects 
    result = bpy.ops.outliner.orphans_purge()
    if result.pop() != "CANCELLED":
        purge_orphans()


def clean_scene():
    # not in Edit Mode
    if bpy.context.active_object and bpy.context.active_object.mode == "EDIT":
        # change into Object mode
        bpy.ops.object.editmode_toggle()

    for obj in bpy.data.objects:
        obj.hide_set(False)
        obj.hide_select = False
        obj.hide_viewport = False

    # select all the object and delete 
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()

    # find all the collections and remove 
    collection_names = [col.name for col in bpy.data.collections]
    for name in collection_names:
        bpy.data.collections.remove(bpy.data.collections[name])

    # delete and recreate the world object
    world_names = [world.name for world in bpy.data.worlds]
    for name in world_names:
        bpy.data.worlds.remove(bpy.data.worlds[name])
    # create a new world data block
    bpy.ops.world.new()
    bpy.context.scene.world = bpy.data.worlds["World"]

    purge_orphans()

# -----------------------------------------------------------

def active_object():
    
    return bpy.context.active_object

# resource: https://blender.stackexchange.com/questions/71641/how-to-manipulate-objects-using-seed-button-in-real-time

def time_seed():
    # random time seed 
    seed = time.time()
    print(f"seed: {seed}")
    random.seed(seed)

    # add the seed value 
    bpy.context.window_manager.clipboard = str(seed)

    return seed


def make_active(obj):
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    # the active object should in the current layer
    bpy.context.view_layer.objects.active = obj


def setup_camera(loc, rot):
    
    bpy.ops.object.camera_add(location=loc, rotation=rot)
    camera = active_object()

    # set the camera as the "active camera" in the scene
    bpy.context.scene.camera = camera

    # set the Focal Length of the camera
    camera.data.lens = 50
    
    # make darker at the corners (edges)
    camera.data.passepartout_alpha = 0.9

    return None 


def set_1080px_square_render_res():

    bpy.context.scene.render.resolution_x = 1080
    bpy.context.scene.render.resolution_y = 1080


def set_scene_props(fps, loop_seconds):

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
    
    # bloom: shinning effect 
    scene.eevee.use_bloom = True
    scene.eevee.bloom_intensity = 0.005

    # set rendering properties
    # create shadows 
    scene.eevee.use_gtao = True 
    scene.eevee.gtao_distance = 4
    scene.eevee.gtao_factor = 5

    scene.eevee.taa_render_samples = 64

    scene.view_settings.look = "Very High Contrast"
    bpy.context.preferences.edit.use_negative_frames = True

    set_1080px_square_render_res()


def setup_scene(i=0):
    fps = 30
    loop_seconds = 6
    frame_count = fps * loop_seconds

    seed = 0
    if seed:
        random.seed(seed)
    else:
        time_seed()

    clean_scene()
    set_scene_props(fps, loop_seconds)
    
    # camera location 
    loc = (0, 0, 7)
    rot = (0, 0, 0)
    setup_camera(loc, rot)

    context = {
        "frame_count": frame_count,
    }

    return context


def make_fcurves_linear():
    for fcurve in bpy.context.active_object.animation_data.action.fcurves:
        for points in fcurve.keyframe_points:
            points.interpolation = "LINEAR"
            # constant speed moving, no easing 


def get_random_color():
    return random.choice(
        [
            [0.48046875, 0.171875, 0.5, 0.99609375],
            [0.3515625, 0.13671875, 0.39453125, 0.99609375],
            [0.2734375, 0.21484375, 0.08984375, 0.99609375],
            [0.5625, 0.45703125, 0.234375, 0.99609375],
            [0.92578125, 0.8828125, 0.77734375, 0.99609375],
            [0.1640625, 0.4921875, 0.13671875, 0.99609375],
            [0.453125, 0.74609375, 0.328125, 0.99609375],
            [0.2734375, 0.21484375, 0.08984375, 0.99609375],
            [0.5625, 0.45703125, 0.234375, 0.99609375],
            [0.92578125, 0.8828125, 0.77734375, 0.99609375],
            [0.1640625, 0.4921875, 0.13671875, 0.99609375],
            [0.453125, 0.74609375, 0.328125, 0.99609375],
            [0.00390625, 0.11328125, 0.15625, 0.99609375],
            [0.0234375, 0.49609375, 0.46875, 0.99609375],
            [0.01953125, 0.51953125, 0.6953125, 0.99609375],
            [0, 0.66796875, 0.78515625, 0.99609375],
            [0, 0.15234375, 0.171875, 0.99609375],
            [0.3203125, 0, 0.12890625, 0.99609375],
            [0.56640625, 0, 0.2265625, 0.99609375],
            [0.99609375, 0, 0.3984375, 0.99609375],
            [0.9453125, 0.640625, 0.33203125, 0.99609375],
            [0.51953125, 0.453125, 0.38671875, 0.99609375],
            [0.84765625, 0.94140625, 0.63671875, 0.99609375],
            [0.30859375, 0.91796875, 0.59375, 0.99609375],
            [0.46484375, 0.76171875, 0.47265625, 0.99609375],
            [0.71875, 0.5390625, 0.546875, 0.99609375],
            [0.40234375, 0.3671875, 0.30859375, 0.99609375],
        ]
    )


def apply_material(obj):
    color = get_random_color()
    mat = bpy.data.materials.new(name="Material")
    mat.use_nodes = True
    mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = color
    mat.node_tree.nodes["Principled BSDF"].inputs["Specular"].default_value = 0
    # add material into the list
    obj.data.materials.append(mat)


def add_lights():
    bpy.ops.object.light_add(type="SUN")
    bpy.context.object.data.energy = 10


def create_circle_control_empty():
    bpy.ops.object.empty_add()
    empty = active_object()
    empty.name = "empty.circle.cntrl" 
    empty.rotation_euler.z = math.radians(random.uniform(0, 360))
    empty.location.z = random.uniform(-3, 1)
    return empty


def animate_object_translation(context, obj):
    
    frame = random.randint(-context["frame_count"], 0)
    obj.location.x = 0
    obj.keyframe_insert("location", frame=frame)

    frame += context["frame_count"]
    
    # move outside
    obj.location.x = random.uniform(5, 5.5)
    obj.keyframe_insert("location", frame=frame)

    fcurves = obj.animation_data.action.fcurves
    location_fcurve = fcurves.find("location")
    # animation loop
    location_fcurve.modifiers.new(type="CYCLES")

    make_fcurves_linear()


def gen_centerpiece(context):

    for _ in range(500):
        empty = create_circle_control_empty()

        bpy.ops.mesh.primitive_circle_add(radius=0.1, fill_type="TRIFAN")
        circle = active_object()
        # apply circles to the empty so that empty can control circles 
        # use empty to determine
        circle.parent = empty

        apply_material(circle)

        animate_object_translation(context, circle)


def main():
    
    context = setup_scene()
    gen_centerpiece(context)
    add_lights()


if __name__ == "__main__":
    main()
