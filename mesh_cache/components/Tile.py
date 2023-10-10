from gem5.components.cachehierarchies.chi.nodes.abstract_node import AbstractNode
from gem5.components.boards.abstract_board import AbstractBoard

from m5.objects import RubySystem, ClockDomain, SubSystem

from .MeshDescriptor import MeshTracker, Coordinate
from .NetworkComponents import RubyRouter, RubyNetworkComponent

class Tile(SubSystem, RubyNetworkComponent):
    def __init__(
        self, 
        board: AbstractBoard,
        ruby_system: RubySystem,
        coordinate: Coordinate,
        mesh_descriptor: MeshTracker
    ) -> None:
        SubSystem.__init__(self=self)
        RubyNetworkComponent.__init__(self=self)

        self._board = board
        self._ruby_system = ruby_system
        self._cache_line_size = board.get_cache_line_size()
        self._mesh_descriptor = mesh_descriptor

        self.cross_tile_router = self.create_router(ruby_system)
        self._mesh_descriptor.add_cross_tile_router(coordinate, self.cross_tile_router)