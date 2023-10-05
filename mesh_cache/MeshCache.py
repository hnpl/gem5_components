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

from .components.L3Slice import L3Slice
from .components.MeshNetwork import MeshNetwork

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
        is_fullsystem: bool
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

        requires(coherence_protocol_required=CoherenceProtocol.CHI)

    @overrides(AbstractCacheHierarchy)
    def incorporate_cache(self, board):

        self.ruby_system = RubySystem()
        self.ruby_system.number_of_virtual_networks = 4
        self.ruby_system.network = MeshNetwork(self.ruby_system)

"""
        # test
        self.l3_slice = L3Slice(
            size = "2MiB",
            associativity = 16,
            network = self.ruby_system.network,
            cache_line_size = board.cache_line_size,
            clk_domain = board.clk_domain
        )
        pass
        """