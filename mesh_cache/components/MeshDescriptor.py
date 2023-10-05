class Coordinate:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
    def get_hash(self):
        return (self.x, self.y)
    def __str__(self):
        return f"({self.x}, {self.y})"

class NodeType:
    EmptyTile = 0
    CoreTile = 1
    MemTile = 2
    DMATile = 3

class MeshNode:
    def __init__(self, coordinate: Coordinate, node_type: NodeType):
        self.coordinate = coordinate
        self.node_type = node_type

class MeshTracker:
    def __init__(self):
        self.grid_tracker = {}
        self.node_router = {}
        self.node_ext_link = {}
    def add_node(self, coordinate: Coordinate, node_type: NodeType):
        new_node = MeshNode(coordinate, node_type)
        assert(not coordinate.get_hash() in self.grid_tracker, "Trying to add an occupied node")
        self.grid_tracker[coordinate.get_hash()] = new_node
    def add_router(self, coordinate: Coordinate, router: RubyRouter):
        assert(coordinate.get_hash() in self.grid_tracker, f"Node with coordiate {coordiate} does not exist")
        self.node_router[coordiate.get_hash()] = router
    def add_ext_link(self, coordiate: Coordinate, ext_link: RubyExtLink):
        assert(coordinate.get_hash() in self.grid_tracker, f"Node with coordiate {coordiate} does not exist")
        self.node_ext_link[coordiate.get_hash()] = ext_link
    def get_node(self, coordiate: Coordiate):
        return self.grid_tracker[coordiate.get_hash()]
    def get_router(self, coordiate: Coordinate):
        return self.node_router[coordiate.get_hash()]
    def get_ext_link(self, coordiate: Coordinate):
        return self.node_ext_link[coordiate.get_hash()]
    def get_width(self):
        max_x = -1
        for x, y in self.grid_tracker.keys():
            max_x = max(x, max_x)
        return max_x + 1
    def get_height(self):
        max_y = -1
        for x, y in self.grid_tracker.keys():
            max_y = max(y, max_y)
        return max_y + 1