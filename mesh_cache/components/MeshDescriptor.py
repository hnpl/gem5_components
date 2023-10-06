from typing import Any

from .NetworkComponents import RubyRouter, RubyExtLink

class Coordinate:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
    def get_hash(self) -> tuple[int, int]:
        return (self.x, self.y)
    def __str__(self) -> str:
        return f"({self.x}, {self.y})"
    @classmethod
    def create_coordinate_from_tuple(cls, t) -> "Coordinate":
        return Coordinate(t[0], t[1])

class NodeType:
    EmptyTile = 0
    CoreTile = 1
    MemTile = 2
    DMATile = 3
    @classmethod
    def to_string(cls, obj: "NodeType") -> str:
        name_map = {
            NodeType.EmptyTile: "EmptyTile",
            NodeType.CoreTile: "CoreTile",
            NodeType.MemTile: "MemTile",
            NodeType.DMATile: "DMATile"
        }
        return name_map[obj]

class MeshNode:
    def __init__(self, coordinate: Coordinate, node_type: NodeType) -> None:
        self.coordinate = coordinate
        self.node_type = node_type
        self.associated_objects = {}
    def add_associated_objects(self, object_name: str, obj: Any) -> None:
        assert(not object_name in self.associated_objects, f"{object_name} exists")
        self.associated_objects[object_name] = obj
    def __str__(self) -> str:
        return f"{str(self.coordinate)}: {NodeType.to_string(self.node_type)}"

class MeshTracker:
    def __init__(self, name: str) -> None:
        self.name = name
        self.grid_tracker = {}
        self.node_cross_tile_router = {}
        self.node_ext_link = {}
    def add_node(self, coordinate: Coordinate, node_type: NodeType) -> None:
        new_node = MeshNode(coordinate, node_type)
        assert(not coordinate.get_hash() in self.grid_tracker, "Trying to add an occupied node")
        self.grid_tracker[coordinate.get_hash()] = new_node
    def add_cross_tile_router(self, coordinate: Coordinate, router: RubyRouter) -> None:
        assert(coordinate.get_hash() in self.grid_tracker, f"Node with coordinate {coordinate} does not exist")
        self.node_cross_tile_router[coordinate.get_hash()] = router
    def add_ext_link(self, coordinate: Coordinate, ext_link: RubyExtLink) -> None:
        assert(coordinate.get_hash() in self.grid_tracker, f"Node with coordinate {coordinate} does not exist")
        self.node_ext_link[coordinate.get_hash()] = ext_link
    def get_sorted_coordinate(self) -> list[Coordinate]:
        coor = list(self.grid_tracker.keys())
        width = self.get_width()
        coor = sorted(coor, key=lambda k: k[1]*width+k[0])
        return coor
    def get_node(self, coordinate: Coordinate) -> MeshNode:
        return self.grid_tracker[coordinate.get_hash()]
    def get_nodes(self) -> list[MeshNode]:
        return list(self.grid_tracker.values())
    def get_cross_tile_router(self, coordinate: Coordinate) -> RubyRouter:
        return self.node_cross_tile_router[coordinate.get_hash()]
    def get_ext_link(self, coordinate: Coordinate) -> RubyExtLink:
        return self.node_ext_link[coordinate.get_hash()]
    def get_tiles_coordinates(self, tile_type: NodeType) -> list[Coordinate]:
        coor = self.get_sorted_coordinate()
        filtered_coor = filter(lambda c: self.grid_tracker[c].node_type == tile_type, coor)
        return list(map(Coordinate.create_coordinate_from_tuple, filtered_coor))
    def get_width(self) -> int:
        max_x = -1
        for x, y in self.grid_tracker.keys():
            max_x = max(x, max_x)
        return max_x + 1
    def get_height(self) -> int:
        max_y = -1
        for x, y in self.grid_tracker.keys():
            max_y = max(y, max_y)
        return max_y + 1
    def __str__(self) -> str:
        s = []
        for coor in self.get_sorted_coordinate():
            s.append(str(self.grid_tracker[coor]))
        return "\n".join(s) + "\n"