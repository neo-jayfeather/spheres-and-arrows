import trimesh
from os.path import splitext as osPathSplitext
import numpy as np
def concatMesh(mesh1, mesh2, meshOut):
  # takes mesh 1 and, concats their vertices, then concats their triangles
  # also makes the triangle mesh indexing start from the last index in the first mesh
  for x in range(len(mesh2.faces)):
    mesh2.faces[x] += len(mesh1.vertices)
  # Concatenate vertices and faces
  meshOut.faces = np.concatenate((mesh1.faces, mesh2.faces), axis=0)
  meshOut.vertices = np.concatenate((mesh1.vertices, mesh2.vertices), axis=0)
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
    self.faces = self.icosphere.faces
class Arrow:
  def __init__(self, bodySize, coords, arrowSize, upDir):
    self.bodyLength, self.bodyRadius = bodySize
    self.coords = coords
    self.arrowLength, self.arrowRadius = arrowSize
    self.direction = upDir
  def create_mesh(self):
    self.cylinder = trimesh.creation.cylinder(radius = self.bodyRadius, height = self.bodyLength, sections = 256)
    self.cone = trimesh.creation.cone(radius = self.arrowRadius, height = self.arrowLength)
    self.mesh = emptyMesh()
    concatMesh(self.cylinder,self.cone,self.mesh)


def main():
  # Sphere parameters
  subDivs = 4
  radius = 10

  # Create sphere objects
  sphere_left = Sphere(subDivs, radius, [-50, 0, 0])
  sphere_right = Sphere(subDivs, radius, [50, 0, 0])
  sphere_middle = Sphere(subDivs, radius, [0,0,0])
  # Create meshes for each sphere (vertices only)
  sphere_left.create_mesh()
  sphere_right.create_mesh()
  sphere_middle.create_mesh()
  newMesh = emptyMesh()
  concatMesh(sphere_left, sphere_right,  newMesh)
  concatMesh(newMesh, sphere_middle, newMesh)

  # Create the final mesh object
  mesh = trimesh.Trimesh(vertices=newMesh.vertices, faces=newMesh.faces)

  # Export the mesh as STL
  mesh.export("two_spheres_combined.stl")

  print("Exported combined spheres to two_spheres_combined.stl")

if __name__ == "__main__":
  main()
