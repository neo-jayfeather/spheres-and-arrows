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
    self.faces = [[0,0,0]]
    self.vertices = [[0,0,0]]

class Arrow:
  def __init__(self, bodySize, coords, arrowSize, upDir):
    self.bodyLength, self.bodyRadius = bodySize
    self.coords = coords
    self.arrowLength, self.arrowRadius = arrowSize
    self.direction = upDir
  def create_mesh(self):
    direction_map = {
      "X" : [2,1,0],
      "Y" : [0,2,1],
      "Z" : [0,1,2]
    }
    multi_map = {
      "-X" : [-1,1,1],
      "-Y" : [1,-1,1],
      "-Z" : [1,1,-1]
    }
  
    self.cylinder = trimesh.creation.cylinder(radius = self.bodyRadius, height = self.bodyLength, sections = 256)
    self.cone = trimesh.creation.cone(radius = self.arrowRadius, height = self.arrowLength, sections = 256)
    self.mesh = emptyMesh()
    self.cone.vertices += [0,0,self.bodyLength]
    self.cylinder.vertices += [0,0,self.bodyLength/2]
    concatMesh(self.cylinder,self.cone,self.mesh)
    self.vertices = self.mesh.vertices
    self.faces = self.mesh.faces
    multiChange = multi_map.get(self.direction, [1,1,1])
    self.direction = self.direction.split('-')[len(self.direction.split('-'))-1]
    dirChange = direction_map.get(self.direction)
    for x in range(len(self.vertices)): # need better rotation algorithm but this works!
      self.vertices[x] = [self.vertices[x][dirChange[0]],self.vertices[x][dirChange[1]],self.vertices[x][dirChange[2]]]
    self.vertices *= multiChange
arrows =  [
  Arrow([30,5],[0,0,0],[7,7],'-Z'),
  Arrow([30,5],[0,0,0],[7,7],"Z"),
  Arrow([30,5],[0,0,0],[7,7],'X'),
  Arrow([30,5],[0,0,0],[7,7],'-X'),
  Arrow([30,5],[0,0,0],[7,7],'Y'),
  Arrow([30,5],[0,0,0],[7,7],'-Y'),
  emptyMesh()
]
totalArrows = len(arrows)-1
for x in range(totalArrows):
  arrows[x].create_mesh()
  concatMesh(arrows[totalArrows],arrows[x], arrows[totalArrows])

output = trimesh.Trimesh(vertices = arrows[totalArrows].vertices, faces = arrows[totalArrows].faces)
output.export("C:\\users\\ncneo\\desktop\\cylinder.stl","stl")