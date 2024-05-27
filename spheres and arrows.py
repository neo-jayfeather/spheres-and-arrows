# yo quiero cantar ahora porque no puedo hacer mas
# no se que hacer con mi vida
import trimesh
from os.path import splitext as osPathSplitext
def exportMesh(oldMesh, fileName):
   extension = osPathSplitext(fileName)[1]
   oldMesh.export(fileName,extension)
class newSphere:
  def __init__(self, subDivs, radius):
    self.subDivs = subDivs
    self.radius = radius
  def createMesh(self):
    self.icosphere = trimesh.creation.icosphere(subdivisons=self.subDivs, radius=self.radius)
    self.mesh = trimesh.Trimesh(vertices=self.icosphere.vertices, faces=self.icosphere.faces)  # Use icosahedron faces
  def exportFile(self, fileName):
     exportMesh(self.mesh,fileName)

x = newSphere(10, 10)
x.createMesh()
x.mesh.export("C:\\users\\ncneo\\desktop\\icosphere89.stl","stl")
x.exportFile("C:\\users\\ncneo\\desktop\\icosphere69.stl")
print(x)

def sphereExport(subDivs, path, filetype):
    # Create the icosphere (replace with your desired subdivisions)
    icosphere = trimesh.creation.icosphere(subdivisions=subDivs)
    filename = f"{path}"
    mesh = trimesh.Trimesh(vertices = icosphere.vertices, faces = icosphere.faces)
    mesh.export(filename, file_type = filetype)
#sphereExport(2, "C:\\users\\ncneo\\desktop\\icosphere.stl", "stl")
'''
# Create the icosphere (replace with your desired subdivisions)
icosphere = trimesh.creation.icosphere(subdivisions=10)

# Specify the filename for the STL export
filename = "C:\\users\\ncneo\\desktop\\icosphere.3mf"

# Export the icosphere to an STL file
mesh = trimesh.Trimesh(vertices = icosphere.vertices, faces = icosphere.faces)

mesh.export(filename, file_type = "3mf")'''

