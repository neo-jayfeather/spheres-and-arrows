import trimesh
from os.path import splitext as osPathSplitext

class newSphere:
  def __init__(self, subDivs, radius):
    self.subDivs = subDivs
    self.radius = radius
  def createSphere(self):
    self.icosphere = trimesh.creation.icosphere(subdivisons=self.subDivs, radius=self.radius)
  def createMesh(self):
    self.mesh = trimesh.Trimesh(vertices = self.icosphere.vertices, faces = self.icosphere.faces)
x = newSphere(10, 10)
x.createSphere()
