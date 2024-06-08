import trimesh
import numpy as np
from skimage.color import lab2rgb

arrowSize = [97,1] # arrow length and width
coneSize = [3,1.5] # arrow tip length and width
subDivs = 4 #sphere subdivisions (20*4^x)
radius = 2 #sphere raidus

def concatMesh(mesh1, mesh2, meshOut, *args):
  """
  Concatenates the vertices and faces of two meshes into a new mesh object.
  Args:
      mesh1 (trimesh.Trimesh): The first mesh to concatenate.
      mesh2 (trimesh.Trimesh): The second mesh to concatenate.
      meshOut (emptyMesh): An empty mesh object to store the combined result.
  """
  new_vertices = np.concatenate((mesh1.vertices, mesh2.vertices), axis=0) #combine vertices
  new_faces = np.concatenate((mesh1.faces, mesh2.faces + len(mesh1.vertices)), axis=0) #combine renumbered faces
  if(args):
    new_colors = np.concatenate((mesh1.colors, mesh2.colors), axis=0)
    meshOut.colors = new_colors
  meshOut.vertices, meshOut.faces = new_vertices, new_faces #lazy code
class emptyMesh:
  def __init__(self):
    self.faces = [[0,0,0]]
    self.vertices = [[0,0,0]]
    self.colors = [[0,0,0,0]]
class Sphere:
  def __init__(self, subDivs, radius, position):
    self.subDivs = subDivs
    self.radius = radius
    self.position = position
    self.colors = [int(value) for value in np.round(lab2rgb(self.position)*255,0)]
  def create_mesh(self):
    self.icosphere = trimesh.creation.icosphere(subdivisions=self.subDivs, radius=self.radius)
    self.vertices = self.icosphere.vertices + self.position  # Apply position shift
    self.faces = self.icosphere.faces
    self.colors = [[self.colors[0],self.colors[1],self.colors[2],255] for _ in range(len(self.faces))]
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
    color_map = {
      "Z": [255, 0  , 0  , 255],
      "-Z":[0  , 255, 0  , 255],
      "Y": [0  , 0  , 255, 255],
      "-Y":[255, 127, 0  , 255],
      "X": [255, 255, 255, 255],
      "-X": [0  , 0  , 0  , 255]
    }
    
    self.cylinder = trimesh.creation.cylinder(radius = self.bodyRadius, height = self.bodyLength, sections = 256)
    self.cone = trimesh.creation.cone(radius = self.arrowRadius, height = self.arrowLength, sections = 256)
    self.mesh = emptyMesh()

    self.direction = self.direction.split('-')[len(self.direction.split('-'))-1]
    dirChange = direction_map.get(self.direction)
    multiChange = multi_map.get(self.direction, [1,1,1])
    cAssign = color_map.get(self.direction)



    self.cone.vertices += [0,0,self.bodyLength]
    self.cylinder.vertices += [0,0,self.bodyLength/2]
    concatMesh(self.cylinder,self.cone,self.mesh)
    self.vertices = self.mesh.vertices
    self.faces = self.mesh.faces

    
    for x in range(len(self.vertices)): # need better rotation algorithm but this works!
      self.vertices[x] = [self.vertices[x][dirChange[0]],self.vertices[x][dirChange[1]],self.vertices[x][dirChange[2]]]
    self.vertices *= multiChange
    self.colors = [cAssign for _ in range(len(self.faces))]


#arrows

arrows =  [
  Arrow(arrowSize,[0,0,50],coneSize,'-Z'),
  Arrow(arrowSize,[0,0,50],coneSize,"Z"),
  Arrow(arrowSize,[0,0,50],coneSize,'X'),
  Arrow(arrowSize,[0,0,50],coneSize,'-X'),
  Arrow(arrowSize,[0,0,50],coneSize,'Y'),
  Arrow(arrowSize,[0,0,50],coneSize,'-Y'),
  emptyMesh()
]
totalArrows = len(arrows)-1
for x in range(totalArrows):
  arrows[x].create_mesh()
  concatMesh(arrows[totalArrows],arrows[x], arrows[totalArrows], True)
# Sphere parameters


spheres = [
  Sphere(subDivs, radius, [94.21, 1.5, 5.42]),
  Sphere(subDivs, radius, [92.28, 2.06, 7.28]),
  Sphere(subDivs, radius, [93.09, 0.22, 14.21]),
  Sphere(subDivs, radius, [85.57, 0.46, 17.75]),
  Sphere(subDivs, radius, [77.9, 3.47, 23.14]),
  Sphere(subDivs, radius, [55.142, 7.78, 26.74]),
  Sphere(subDivs, radius, [42.47, 12.33, 20.53]),
  Sphere(subDivs, radius, [30.68, 11.67, 13.33]),
  Sphere(subDivs, radius, [21.07, 2.69, 5.97]),
  Sphere(subDivs, radius, [14.61, 1.48, 3.53]),
]
# Create meshes for each sphere (vertices only)
newMesh = emptyMesh()
concatMesh(newMesh, arrows[totalArrows], newMesh, True)
for x in range(len(spheres)):
  spheres[x].create_mesh()
  concatMesh(newMesh, spheres[x], newMesh, True)

addColors = newMesh.colors
# Create the combined mesh
for x in range(len(newMesh.vertices)):
  a = newMesh.vertices[x]
  newMesh.vertices[x] = [a[1], a[0], a[2]]
mesh = trimesh.Trimesh(vertices=newMesh.vertices, faces=newMesh.faces)

for x in range(len(addColors)):
  mesh.visual.face_colors[x] = addColors[x]  # VERY DUMB BUT DO NOT TOUCH

# Export the mesh
mesh.export("two_spheres_combined.glb", file_type = "glb")
print("Exported combined spheres to two_spheres_combined.glb")