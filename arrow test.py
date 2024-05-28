import trimesh
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
    self.cone.vertices += [0,0,self.bodyLength]
    self.cylinder.vertices += [0,0,self.bodyLength/2]
    concatMesh(self.cylinder,self.cone,self.mesh)
    self.vertices = self.mesh.vertices
    self.faces = self.mesh.faces
arrow = Arrow([30,5],[0,0,0],[7,7],'X')
arrow.create_mesh()
output = trimesh.Trimesh(vertices = arrow.vertices, faces = arrow.faces)
output.export("C:\\users\\ncneo\\desktop\\cylinder.stl","stl")