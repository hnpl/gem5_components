from gem5.utils.requires import requires
from gem5.utils.override import overrides
from gem5.coherence_protocol import CoherenceProtocol
from gem5.components.boards.abstract_board import AbstractBoard

from gem5.components.cachehierarchies.ruby.abstract_ruby_cache_hierarchy import AbstractRubyCacheHierarchy
from gem5.components.cachehierarchies.abstract_three_level_cache_hierarchy import AbstractThreeLevelCacheHierarchy
from gem5.components.cachehierarchies.abstract_cache_hierarchy import AbstractCacheHierarchy
from gem5.components.cachehierarchies.chi.nodes.dma_requestor import DMARequestor
from gem5.components.cachehierarchies.chi.nodes.memory_controller import MemoryController
from gem5.components.cachehierarchies.chi.nodes.abstract_node import AbstractNode

from m5.objects import RubySystem

from .components.CoreTile import CoreTile
from .components.L3Slice import L3Slice
from .components.MeshDescriptor import MeshTracker, NodeType
from .components.MeshNetwork import MeshNetwork
from .components.NetworkComponents import RubyNetworkComponent
from .utils.SizeArithmetic import SizeArithmetic

class MeshCache(AbstractRubyCacheHierarchy, AbstractThreeLevelCacheHierarchy):
    def __init__(
        self,
        l1i_size: str,
        l1i_assoc: int,
        l1d_size: str,
        l1d_assoc: int,
        l2_size: str,
        l2_assoc: int,
        l3_size: str,
        l3_assoc: int,
        num_core_complexes: int,
        is_fullsystem: bool,
        mesh_descriptor: MeshTracker
    ):
        AbstractRubyCacheHierarchy.__init__(self=self)
        AbstractThreeLevelCacheHierarchy.__init__(
            self=self,
            l1i_size=l1i_size,
            l1i_assoc=l1i_assoc,
            l1d_size=l1d_size,
            l1d_assoc=l1d_assoc,
            l2_size=l2_size,
            l2_assoc=l2_assoc,
            l3_size=l3_size,
            l3_assoc=l3_assoc,
        )

        self._num_core_complexes = num_core_complexes
        self._is_fullsystem = is_fullsystem
        self._mesh_descriptor = mesh_descriptor

        # temporary objects
        self._core_tiles = []

        print(self._mesh_descriptor)

        requires(coherence_protocol_required=CoherenceProtocol.CHI)

    @overrides(AbstractCacheHierarchy)
    def incorporate_cache(self, board: AbstractBoard) -> None:
        self._setup_ruby_system()
        self._get_board_info(board)

        self._create_core_tiles(board)

        self._finalize_ruby_system()

    def _get_board_info(self, board: AbstractBoard) -> None:
        self._cache_line_size = board.cache_line_size
        self._clk_domain = board.clk_domain

    # should be called at the BEGINNING of incorporate_cache()
    def _setup_ruby_system(self) -> None:
        self.ruby_system = RubySystem()
        self.ruby_system.number_of_virtual_networks = 4
        self.ruby_system.network = MeshNetwork(
            ruby_system = self.ruby_system,
            mesh_descriptor = self._mesh_descriptor
        )
        self.ruby_system.network.number_of_virtual_networks = 4
        self.ruby_system.num_of_sequencers = 0

    # should be called at the END of incorporate_cache()
    def _finalize_ruby_system(self) -> None:
        self.ruby_system.network.int_links = self.ruby_system.network._int_links
        self.ruby_system.network.ext_links = self.ruby_system.network._ext_links
        self.ruby_system.network.routers = self.ruby_system.network._routers
        self.ruby_system.network.setup_buffers()

    def _create_core_tiles(self, board: AbstractBoard) -> None:
        core_tile_coordinates = self._mesh_descriptor.get_tiles_coordinates(NodeType.CoreTile)
        cores = board.get_processor().get_cores()
        num_l3_slices = len(cores)
        l3_slice_size = (SizeArithmetic(self._l3_size) // num_l3_slices).get()
        self.core_tiles = [CoreTile(
            board = board,
            ruby_system = self.ruby_system,
            core = core,
            core_id = core_id,
            l1i_size = self._l1i_size,
            l1i_associativity = self._l1i_assoc,
            l1d_size = self._l1d_size,
            l1d_associativity = self._l1d_assoc,
            l2_size = self._l2_size,
            l2_associativity = self._l2_assoc,
            l3_slice_size = l3_slice_size,
            l3_associativity = self._l3_assoc,
            coordinate = core_tile_coordinate
        ) for core_id, (core, core_tile_coordinate) in enumerate(zip(cores, core_tile_coordinates))]
        for tile in self.core_tiles:
            self.ruby_system.network.incorporate_ruby_subsystem(tile)
        self.ruby_system.num_of_sequencers += len(cores)

"""
    def _create_L3_slices(self):
        # create the cache slices
        self.l3_slices = [L3Slice(
            size = self._l3_size,
            associativity = self._l3_assoc,
            ruby_system = self.ruby_system,
            cache_line_size = self._cache_line_size,
            clk_domain = self._clk_domain
        ) for i in range(self._per_ccd_num_cores)]

        # create one router per cache slice
        self.l3_routers = [
            RubyRouter(self.ruby_system)
            for i in range()
        ]

        # router <-----ExtLink-----> cache_slice
        self.l3_router_links = [RubyExtLink(
            ext_node=l3_slice,
            int_node=l3_router
        ) for l3_slice, l3_router in zip(self.l3_slices, self.l3_routers)]

        # add created links and routers to the network
        for l3_router in self.l3_routers:
            self._add_router(self.l3_router)
        for link in self.l3_router_links:
            self._add_ext_link(link)
"""