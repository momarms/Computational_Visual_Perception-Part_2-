import bpy
import math

# File path
obj_file_path = r'D:\FAU\Studies\4- WS 2023\Computational Visual Perception\Project\Part 2\Dataset\colored_cloths\1.obj'
output_directory = r'D:\FAU\Studies\4- WS 2023\Computational Visual Perception\Project\Part 2\Distance_Rendering'

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

# Add a camera
location = (2, 2, 2)
rotation = (math.radians(50), math.radians(0), math.radians(135))
bpy.ops.object.camera_add(location=location, rotation = rotation)
camera_object = bpy.context.object
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

# Set the output path for the rendered image
bpy.context.scene.render.filepath = output_directory + "\\1"

# Render the image
bpy.ops.render.render(write_still=True)