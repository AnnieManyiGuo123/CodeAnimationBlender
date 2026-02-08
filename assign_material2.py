# assign materials in detailed

import bpy
import math
import random

# always restart
def partially_clean_the_scene():
    # select all object 
    bpy.ops.object.select_all(action="SELECT")

    # delete all selected objects in the scene
    bpy.ops.object.delete()

    # remove data that was connected to the objects 
    bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)

# reference: Blender API "node"
# create different nodes (node can control different part of the material)
# connect notes
# assign to the object

def create_noise_mask(material):

    node_location_x_step = 300
    node_location_x = -node_location_x_step

    # create a Color Ramp node
    color_ramp_node = material.node_tree.nodes.new(type="ShaderNodeValToRGB")
    color_ramp_node.color_ramp.elements[0].position = 0.45
    color_ramp_node.color_ramp.elements[1].position = 0.5
    color_ramp_node.location.x = node_location_x
    node_location_x -= node_location_x_step

    # create a Noise Texture node
    noise_texture_node = material.node_tree.nodes.new(type="ShaderNodeTexNoise")
    noise_texture_node.inputs["Scale"].default_value = random.uniform(1.0, 20.0)
    noise_texture_node.location.x = node_location_x
    node_location_x -= node_location_x_step

    # create a Mapping node
    mapping_node = material.node_tree.nodes.new(type="ShaderNodeMapping")
    mapping_node.inputs["Rotation"].default_value.x = math.radians(random.uniform(0.0, 360.0))
    mapping_node.inputs["Rotation"].default_value.y = math.radians(random.uniform(0.0, 360.0))
    mapping_node.inputs["Rotation"].default_value.z = math.radians(random.uniform(0.0, 360.0))
    mapping_node.location.x = node_location_x
    node_location_x -= node_location_x_step

    # create a Texture Coordinate node
    texture_coordinate_node = material.node_tree.nodes.new(type="ShaderNodeTexCoord")
    texture_coordinate_node.location.x = node_location_x

    # connect the nodes
    material.node_tree.links.new(noise_texture_node.outputs["Color"], color_ramp_node.inputs["Fac"])
    material.node_tree.links.new(mapping_node.outputs["Vector"], noise_texture_node.inputs["Vector"])
    material.node_tree.links.new(texture_coordinate_node.outputs["Generated"], mapping_node.inputs["Vector"])

    return color_ramp_node


def create_material(name):
    # create new material
    material = bpy.data.materials.new(name=name)
    # enable nodes
    material.use_nodes = True

    # reference to the "shader node"
    principled_bsdf_node = material.node_tree.nodes["Principled BSDF"]

    # set the base color 
    principled_bsdf_node.inputs["Base Color"].default_value = (0.8, 0.120827, 0.0074976, 1)

    # set the metallic value 
    principled_bsdf_node.inputs["Metallic"].default_value = 1.0

    color_ramp_node = create_noise_mask(material)

    material.node_tree.links.new(color_ramp_node.outputs["Color"], principled_bsdf_node.inputs["Roughness"])

    return material


def add_mesh():
    # create an ico sphere
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=5)
    
    # shade smooth
    bpy.ops.object.shade_smooth()
    
    # reference to mesh object
    mesh_obj = bpy.context.active_object

    return mesh_obj


def main():

    partially_clean_the_scene()

    name = "my_generated_material"
    material = create_material(name)

    mesh_obj = add_mesh()

    # apply the material to the mesh object
    mesh_obj.data.materials.append(material)


main()
