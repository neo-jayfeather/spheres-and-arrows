import trimesh
from os.path import splitext as osPathSplitext
import numpy as np
def concatMesh(mesh1, mesh2, meshOut):
  """
  Concatenates the vertices and faces of two meshes into a new mesh object.

  Args:
      mesh1 (trimesh.Trimesh): The first mesh to concatenate.
      mesh2 (trimesh.Trimesh): The second mesh to concatenate.
      meshOut (emptyMesh): An empty mesh object to store the combined result.
  """
  new_vertices = np.concatenate((mesh1.vertices, mesh2.vertices), axis=0) #combine vertices
  new_faces = np.concatenate((mesh1.faces, mesh2.faces + len(mesh1.vertices)), axis=0) #combine renumbered faces
  meshOut.vertices, meshOut.faces = new_vertices, new_faces #lazy code
class emptyMesh:
  def __init__(self):
    self.faces = [[0,0,0]]
    self.vertices = [[0,0,0]]
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


#arrows
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

# Sphere parameters
subDivs = 4
radius = 15

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
concatMesh(newMesh, arrows[totalArrows], newMesh)
# Create the final mesh object
mesh = trimesh.Trimesh(vertices=newMesh.vertices, faces=newMesh.faces)
# Export the mesh as STL
mesh.export("two_spheres_combined.stl")

print("Exported combined spheres to two_spheres_combined.stl")
