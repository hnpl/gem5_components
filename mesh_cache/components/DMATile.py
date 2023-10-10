from gem5.components.boards.abstract_board import AbstractBoard
from gem5.components.cachehierarchies.chi.nodes.dma_requestor import DMARequestor
from gem5.components.cachehierarchies.chi.nodes.memory_controller import MemoryController

from m5.objects import SubSystem, RubySystem, NULL, RubyController, AddrRange, Port, RubySequencer

from .MeshDescriptor import Coordinate, MeshTracker
from .Tile import Tile

class DMATile(Tile):
    def __init__(self,
        board: AbstractBoard,
        ruby_system: RubySystem,
        coordinate: Coordinate,
        mesh_descriptor: MeshTracker,
        dma_port: Port,
        dma_id:int
    ):
        Tile.__init__(self=self, board=board, ruby_system=ruby_system, coordinate=coordinate, mesh_descriptor=mesh_descriptor)

        self.dma_controller = DMARequestor(
            network=ruby_system.network,
            cache_line_size=board.get_cache_line_size(),
            clk_domain=board.get_clock_domain()
        )
        self.dma_controller.ruby_system = ruby_system

        self.dma_controller.sequencer = RubySequencer(
            version = self._ruby_system.network.get_next_sequencer_id(),
            in_ports = dma_port,
            dcache = NULL,
            ruby_system = ruby_system
        )

        self._create_links()

    def _create_links(self):
        self.dma_router = self.create_router(self._ruby_system)
        self.dma_router_link = self.create_ext_link(self.dma_controller, self.dma_router)
        self.dma_router_to_cross_tile_router = self.create_int_link(self.dma_router, self.cross_tile_router)
        self.cross_tile_router_to_dma_router = self.create_int_link(self.cross_tile_router, self.dma_router)
