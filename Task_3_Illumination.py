import bpy
import math
from math import radians, sin, cos
from mathutils import Vector

# Counter
total_images_rendered = 0

for obj_index in range (1, 2):
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
    bpy.ops.import_scene.obj(filepath=obj_file_path)
    print(f"Imported {obj_file_path} successfully.")

    # Add camera
    cam_location = (0, 0, 2)
    bpy.ops.object.camera_add(location=cam_location)
    camera_object = bpy.context.object
    target_point = Vector((0, 0, -0.5))
    bpy.context.scene.camera = camera_object

    # Update the scene
    bpy.context.view_layer.update()

    # Set render settings
    bpy.context.scene.render.resolution_x = 512
    bpy.context.scene.render.resolution_y = 512
    bpy.context.scene.render.image_settings.file_format = 'PNG'
    bpy.context.scene.render.image_settings.color_mode = 'BW'
    bpy.context.scene.render.image_settings.color_depth = '8'
    bpy.context.scene.render.image_settings.use_zbuffer = False

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
        # Keep the camera view at target point
        cam_direction = camera_object.location - target_point
        rot_quat = cam_direction.to_track_quat('Z', 'Y')
        camera_object.rotation_euler = rot_quat.to_euler()

        # Set the output path for the rendered image
        total_images_rendered += 1
        bpy.context.scene.render.filepath = f"{output_directory}\\{total_images_rendered}"

        # Render the image
        bpy.ops.render.render(write_still=True)