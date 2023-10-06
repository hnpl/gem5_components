from m5.objects import ClockDomain
from m5.objects import RubyCache, RubyNetwork, RubySequencer, RubyController, RubySystem

from gem5.components.boards.abstract_board import AbstractBoard
from gem5.components.processors.abstract_core import AbstractCore
from gem5.components.cachehierarchies.chi.nodes.abstract_node import AbstractNode

class L1Cache(AbstractNode):
    def __init__(
        self,
        size: str,
        associativity: int,
        #network: RubyNetwork,
        ruby_system: RubySystem,
        core: AbstractCore,
        cache_line_size: int,
        clk_domain: ClockDomain
    ):
        super().__init__(ruby_system.network, cache_line_size)

        self.cache = RubyCache(
            size=size, assoc=associativity, start_index_bit=self.getBlockSizeBits(),
            ruby_system=ruby_system
        )
        self.ruby_system = ruby_system

        self.clk_domain = clk_domain
        self.send_evictions = core.requires_send_evicts()
        self.use_prefetcher = False

        # Only applies to home nodes
        self.is_HN = False
        self.enable_DMT = False
        self.enable_DCT = False

        self.allow_SD = True
        # Prevent forwarding since I have no idea whether it should be T/F
        self.fwd_unique_on_readshared = False

        self.alloc_on_seq_acc = True
        # Guess: Probably useful for DMA
        self.alloc_on_seq_line_write = False

        self.alloc_on_readshared = True
        self.alloc_on_readunique = True
        self.alloc_on_readonce = True
        self.alloc_on_writeback = False  # Should never happen in an L1

        ###########################
        # Don't apply to L1
        self.dealloc_on_unique = False
        self.dealloc_on_shared = False
        self.dealloc_backinv_unique = False
        self.dealloc_backinv_shared = False
        ###########################

        # Some reasonable default TBE params
        self.number_of_TBEs = 16
        self.number_of_repl_TBEs = 16
        self.number_of_snoop_TBEs = 4
        self.number_of_DVM_TBEs = 16
        self.number_of_DVM_snoop_TBEs = 4
        self.unify_repl_TBEs = False