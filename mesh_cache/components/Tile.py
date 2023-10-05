from .NetworkComponents import RubyRouter, RubyNetworkComponent

class Tile(AbstractNode, RubyNetworkComponent):
    def __init__(self, network: RubyNetwork, cache_line_size: int):
        AbstractNode.__init__(self=self, network=network, cache_line_size=cache_line_size)
        RubyNetworkComponent.__init__(self=self)
        self.cross_tile_router = RubyRouter(self)
        self._add_router(self.cross_tile_router)