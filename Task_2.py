import cv2 as cv
import numpy as np
import openmesh as om
import os
from scipy.spatial import KDTree
import tripy

# Working directory
current_path = os.getcwd()
print(current_path)

project_dir = r'D:\FAU\Studies\4- WS 2023\Computational Visual Perception\Project\Part 2'

try:
    os.chdir(project_dir)
    print("Changed Working Directory to:", os.getcwd())
except FileNotFoundError:
    print("The specified directory does not exist.")
except Exception as e:
    print("An error occurred:", e)

# Load the cloths and objects
cloth_mesh = om.read_trimesh(r'Dataset\cloth\1.obj')
object_mesh = om.read_trimesh(r'Dataset\objects\1.obj')

# Vertex positions from the meshes
cloth_vertices = np.array([cloth_mesh.point(v) for v in cloth_mesh.vertices()])
object_vertices = np.array([object_mesh.point(v) for v in object_mesh.vertices()])
print('Cloth vertices: ', cloth_vertices.shape)
print('Object vertices: ', object_vertices.shape)

# Triangulate the object mesh
object_triangles = object_mesh.face_vertex_indices()

# KDTree for nearest neighbor on the object vertices
object_kdtree = KDTree(object_vertices)

# Array to store distances
distances = np.zeros(len(cloth_vertices))

# For each point on the cloth mesh
for i, cloth_vertex in enumerate(cloth_vertices):
    # Find the index of the nearest vertex on the object mesh
    _, object_vertex_index = object_kdtree.query(cloth_vertex)

    # Get the coordinates of the nearest object vertex
    nearest_object_vertex = object_vertices[object_vertex_index]

    # Calculate the distance from the cloth vertex to the nearest object vertex
    distance = np.linalg.norm(nearest_object_vertex - cloth_vertex)

    # Store the distance in the array
    distances[i] = distance

    # print("Cloth Vertex:", cloth_vertex)
    # print("Nearest Point on Object:", object_triangle_vertices[np.argmin(point_distances)])
    # print("Distance:", min_distance)
    # print("---")

# Distances Array
print("Distances Array:", distances.shape)
print(distances)

min_distance = np.min(distances)
max_distance = np.max(distances)

print("Min Distance (Cloth - Object):", min_distance)
print("Max Distance (Cloth - Object):", max_distance)

# Clip distances between 0 - 0.1
clipped_distances = np.clip(distances, 0, 0.1)

min_clip_distance = np.min(clipped_distances)
max_clip_distance = np.max(clipped_distances)

print("Min distance after clipping (Cloth - Object):", min_clip_distance)
print("Max distance after clipping (Cloth - Object):", max_clip_distance)

# Scale distances to 0 - 1
scaled_distances = clipped_distances / 0.1

min_scale_distance = np.min(scaled_distances)
max_scale_distance = np.max(scaled_distances)

print("Min distance after scaling (0 - 1):", min_scale_distance)
print("Max distance after scaling (0 - 1):", max_scale_distance)

# Convert to normalized grayscale (Distance 0 = White, Distance 1 = Black)
gray_values = 1 - scaled_distances

min_gray = np.min(gray_values)
max_gray = np.max(gray_values)

print("Min after grayscale conversion:", min_gray)
print("Max after grayscale conversion:", max_gray)

