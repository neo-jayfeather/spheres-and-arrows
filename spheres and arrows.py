import trimesh
from os.path import splitext as osPathSplitext
import numpy as np
class emptyMesh:
  def __init__(self):
    self.faces = []
    self.vertices = []
class Sphere:
  def __init__(self, subDivs, radius, position):
    self.subDivs = subDivs
    self.radius = radius
    self.position = position

  def create_mesh(self):
    self.icosphere = trimesh.creation.icosphere(subdivisions=self.subDivs, radius=self.radius)
    self.vertices = self.icosphere.vertices + self.position  # Apply position shift

  def combine_mesh(self, other_sphere):
    for x in range(len(other_sphere.icosphere.faces)):
      other_sphere.icosphere.faces[x] += len(self.vertices)
    try:
      self.faces = np.concatenate((self.faces, other_sphere.icosphere.faces), axis=0)
    except:
      self.faces = np.concatenate((self.icosphere.faces, other_sphere.icosphere.faces), axis=0)
    #offset = len(self.vertices) // 3  # Number of vertices in the first sphere
    self.vertices = np.concatenate((self.vertices, other_sphere.vertices), axis=0)
def concatMesh(mesh1, mesh2, meshOut):
  # takes mesh 1 and, concats their vertices, then concats their triangles
  # also makes the triangle mesh indexing start from the last index in the first mesh
  # 
  for x in range(len(mesh2.faces)):
      mesh2.faces[x] += len(mesh1.vertices)
  meshOut.faces = np.concatenate((mesh1.faces, mesh2.faces), axis=0)
  meshOut.vertices = np.concatenate((mesh1.vertices, mesh2.vertices), axis=0)
def main():
  # Sphere parameters
  subDivs = 4
  radius = 10

  # Sphere positions
  sphere_left_pos = [-50, 0, 0]
  sphere_right_pos = [50, 0, 0]

  # Create sphere objects
  sphere_left = Sphere(subDivs, radius, sphere_left_pos)
  sphere_right = Sphere(subDivs, radius, sphere_right_pos)
  sphere_middle = Sphere(subDivs, radius, [0,0,0])
  # Create meshes for each sphere (vertices only)
  sphere_left.create_mesh()
  sphere_right.create_mesh()
  sphere_middle.create_mesh()
  newMesh = emptyMesh()
  concatMesh(sphere_left.icosphere,sphere_right.icosphere,  newMesh)
  # Create the final mesh object
  mesh = trimesh.Trimesh(vertices=newMesh.vertices, faces=newMesh.faces)

  # Export the mesh as STL
  mesh.export("two_spheres_combined.stl")

  print("Exported combined spheres to two_spheres_combined.stl")

if __name__ == "__main__":
  main()
