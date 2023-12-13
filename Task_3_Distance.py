import bpy
import math
from math import radians, sin, cos
from mathutils import Vector

# Counter
total_images_rendered = 0

# Switch to Object Mode
bpy.ops.object.mode_set(mode='OBJECT')

for obj_index in range(1, 101):
    # File path
    obj_file_path = f'D:\\FAU\\Studies\\4- WS 2023\\Computational Visual Perception\\Project\\Part 2\\Dataset\\colored_cloths\\{obj_index}.obj'
    output_directory = f'D:\\FAU\\Studies\\4- WS 2023\\Computational Visual Perception\\Project\\Part 2\\Distance_Rendering'

    # Delete any existing meshes
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.delete()

    # Delete any existing light source
    bpy.ops.object.select_by_type(type='LIGHT')
    bpy.ops.object.delete()

    # Delete any existing camera
    bpy.ops.object.select_by_type(type='CAMERA')
    bpy.ops.object.delete()

    # Import .obj file
    bpy.ops.wm.obj_import(filepath=obj_file_path)
    print(f"Imported {obj_file_path} successfully.")

    # Switch to the imported mesh object
    obj = bpy.context.active_object

    # Add camera
    cam_location = (0, 0, 2)
    bpy.ops.object.camera_add(location=cam_location)
    camera_object = bpy.context.object
    target_point = Vector((0, 0, -0.5))
    bpy.context.scene.camera = camera_object

    # Set render settings
    bpy.context.scene.render.resolution_x = 512
    bpy.context.scene.render.resolution_y = 512
    bpy.context.scene.render.image_settings.file_format = 'PNG'
    bpy.context.scene.render.image_settings.color_mode = 'BW'
    bpy.context.scene.render.image_settings.color_depth = '8'
    # bpy.context.scene.render.image_settings.use_zbuffer = True
    # bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.preferences.addons['cycles'].preferences.compute_device_type = 'CUDA'

    # Set background color
    bpy.context.scene.world.node_tree.nodes["Background"].inputs["Color"].default_value = (1, 1, 1, 1)

    # Check if there is a material
    if len(obj.data.materials) == 0:
        # Create a new material
        material = bpy.data.materials.new(name="Material")
        obj.data.materials.append(material)

        # Assign the material to the object
        obj.active_material = material

        # Get the material
        material = obj.active_material
        material.use_nodes = True
        nodes = material.node_tree.nodes
        links = material.node_tree.links

        # Clear existing nodes
        nodes.clear()

        # Create an Attribute node to get the color attribute
        attribute_node = nodes.new(type='ShaderNodeAttribute')
        attribute_node.location = (-200, 0)
        attribute_node.attribute_name = 'Color'
        
        # Create a Shader to RGB node
        shader_to_rgb_node = nodes.new(type='ShaderNodeShaderToRGB')
        shader_to_rgb_node.location = (0, 0)

        # Link Attribute node to Shader to RGB node
        links.new(attribute_node.outputs[0], shader_to_rgb_node.inputs[0])

        # Emission Shader for ambient light (no shading)
        emission_shader_node = nodes.new(type='ShaderNodeEmission')
        emission_shader_node.location = (200, 0)
        links.new(shader_to_rgb_node.outputs[0], emission_shader_node.inputs[0])

        # Create an Output Material node
        output_node = nodes.new(type='ShaderNodeOutputMaterial')
        output_node.location = (400, 0)

        # Link the shader to Output Material node
        links.new(emission_shader_node.outputs[0], output_node.inputs[0])

    # Rotate camera around object and capture frames
    num_frames = 50
    rotation_radius = 4
    for img_index in range(num_frames):
        angle = radians((img_index / num_frames) * 360)
        camera_object.location = (
            rotation_radius * cos(angle),
            rotation_radius * sin(angle),
            cam_location[2],
        )
        
        # Keep the camera view at the target point
        cam_direction = camera_object.location - target_point
        rot_quat = cam_direction.to_track_quat('Z', 'Y')
        camera_object.rotation_euler = rot_quat.to_euler()

        # Set the output path for the rendered image
        total_images_rendered += 1
        bpy.context.scene.render.filepath = f"{output_directory}\\{total_images_rendered}"

        # Render the image
        bpy.ops.render.render(write_still=True)