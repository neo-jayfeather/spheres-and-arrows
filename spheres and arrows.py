import trimesh
from os.path import splitext as osPathSplitext
import numpy as np

class Sphere:
  def __init__(self, subDivs, radius, position):
    self.subDivs = subDivs
    self.radius = radius
    self.position = position

  def create_mesh(self):
    self.icosphere = trimesh.creation.icosphere(subdivisions=self.subDivs, radius=self.radius)
    self.vertices = self.icosphere.vertices + self.position  # Apply position shift

  def combine_mesh(self, other_sphere):
    print(len(self.vertices))
    
    for x in range(len(other_sphere.icosphere.faces)):
      other_sphere.icosphere.faces[x] += len(self.vertices)
    
    #offset = len(self.vertices) // 3  # Number of vertices in the first sphere
    self.vertices = np.concatenate((self.vertices, other_sphere.vertices), axis=0)
    self.faces = np.concatenate((self.icosphere.faces, other_sphere.icosphere.faces), axis=0)
def main():
  # Sphere parameters
  subDivs = 4
  radius = 10

  # Sphere positions
  sphere_left_pos = [-50, 0, 0]
  sphere_right_pos = [50, 0, 0]

  # Create sphere objects
  sphere_left = Sphere(1, radius, sphere_left_pos)
  sphere_right = Sphere(subDivs, radius, sphere_right_pos)
  sphere_middle = Sphere(2, radius, [0,0,0])
  # Create meshes for each sphere (vertices only)
  sphere_left.create_mesh()
  sphere_right.create_mesh()
  sphere_middle.create_mesh()
  # Combine sphere meshes into a single mesh
  sphere_left.combine_mesh(sphere_right)
  sphere_left.combine_mesh(sphere_middle)

  # Create the final mesh object
  mesh = trimesh.Trimesh(vertices=sphere_left.vertices, faces=sphere_left.faces)

  # Export the mesh as STL
  mesh.export("two_spheres_combined.stl")

  print("Exported combined spheres to two_spheres_combined.stl")

if __name__ == "__main__":
  main()
