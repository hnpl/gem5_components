from gem5.components.cachehierarchies.chi.nodes.abstract_node import AbstractNode
from gem5.components.boards.abstract_board import AbstractBoard

from m5.objects import RubySystem, ClockDomain, SubSystem

from .NetworkComponents import RubyRouter, RubyNetworkComponent

class Tile(SubSystem, RubyNetworkComponent):
    def __init__(
        self, 
        board: AbstractBoard,
        ruby_system: RubySystem,
        cache_line_size: int
    ) -> None:
        SubSystem.__init__(self=self)
        RubyNetworkComponent.__init__(self=self)

        self.cross_tile_router = RubyRouter(ruby_system.network)
        self._add_router(self.cross_tile_router)