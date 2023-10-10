from .MeshDescriptor import *

class PrebuiltMesh:
    @classmethod
    def getMesh0(cls, name):
        mesh = MeshTracker(name=name)
        mesh.add_node(Coordinate(x = 0, y = 0), NodeType.CoreTile)
        mesh.add_node(Coordinate(x = 0, y = 1), NodeType.MemTile)
        return mesh
    @classmethod
    def getMesh1(cls, name):
        mesh = MeshTracker(name=name)
        mesh.add_node(Coordinate(x = 0, y = 0), NodeType.CoreTile)
        mesh.add_node(Coordinate(x = 0, y = 1), NodeType.CoreTile)
        mesh.add_node(Coordinate(x = 0, y = 2), NodeType.CoreTile)
        mesh.add_node(Coordinate(x = 0, y = 3), NodeType.CoreTile)
        mesh.add_node(Coordinate(x = 1, y = 0), NodeType.CoreTile)
        mesh.add_node(Coordinate(x = 1, y = 1), NodeType.CoreTile)
        mesh.add_node(Coordinate(x = 1, y = 2), NodeType.CoreTile)
        mesh.add_node(Coordinate(x = 1, y = 3), NodeType.CoreTile)
        return mesh
