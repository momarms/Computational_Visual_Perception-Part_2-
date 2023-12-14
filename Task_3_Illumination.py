import bpy
import math
from math import radians, sin, cos
from mathutils import Vector
import random

# Reproducible randomization
random_seed = 42
random.seed(random_seed)

# Counter
total_images_rendered = 0

# Check if there is an active object
if bpy.context.active_object:
    # Switch to Object Mode
    bpy.ops.object.mode_set(mode='OBJECT')

for obj_index in range (1, 101):
    # File path
    obj_file_path = f'D:\\FAU\\Studies\\4- WS 2023\\Computational Visual Perception\\Project\\Part 2\\Dataset\\colored_cloths\\{obj_index}.obj'
    output_directory = f'D:\\FAU\\Studies\\4- WS 2023\\Computational Visual Perception\\Project\\Part 2\\Illumination_Rendering'

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

    # Add camera
    cam_location = (0, 0, 2)
    bpy.ops.object.camera_add(location=cam_location)
    camera_object = bpy.context.object
    target_point = Vector((0, 0, -0.5))
    bpy.context.scene.camera = camera_object
    
    # Add light source
    bpy.ops.object.light_add(type='POINT', location=(0, 0, 2))
    light_object = bpy.context.object
    light_object.data.energy = 500
 
    # Update the scene
    bpy.context.view_layer.update()

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
    bpy.context.scene.world.node_tree.nodes["Background"].inputs["Color"].default_value = (0, 0, 0, 1)
     
    # Change scene and render the images
    num_frames = 50
    rotation_radius = 4
    light_angle_range = 45
    
    for img_index in range(num_frames):
        cam_angle = radians((img_index / num_frames) * 360)
        
        # Rotate camera around the object
        camera_object.location = (
            rotation_radius * cos(cam_angle),
            rotation_radius * sin(cam_angle),
            cam_location[2],
        )
        
        # Keep the camera view at target point
        cam_direction = camera_object.location - target_point
        rot_quat = cam_direction.to_track_quat('Z', 'Y')
        camera_object.rotation_euler = rot_quat.to_euler()
        
        # Change light source location
        light_angle = cam_angle + radians(random.uniform(-light_angle_range, light_angle_range))
        
        light_object.location = (
            rotation_radius * cos(light_angle),
            rotation_radius * sin(light_angle),
            light_object.location[2],
        )
        
        # Set the output path for the rendered image
        total_images_rendered += 1
        bpy.context.scene.render.filepath = f"{output_directory}\\{total_images_rendered}"

        # Render the image
        bpy.ops.render.render(write_still=True)