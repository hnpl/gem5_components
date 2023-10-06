from m5.objects import ClockDomain, NULL
from m5.objects import RubyCache, RubyNetwork, RubySequencer, RubyController, RubySystem

from gem5.components.cachehierarchies.chi.nodes.abstract_node import AbstractNode

class L2Cache(AbstractNode):
    """This cache assumes the CPU-side L1 cache is inclusive (no clean WBs)
    and that the L3 is tracking all tags in the L1/L2.

    This cache also assumes the L3 is a victim cache, so it needs to writeback
    clean and dirty data.
    """

    def __init__(
        self,
        size: str,
        associativity: int,
        #network: RubyNetwork,
        ruby_system: RubySystem,
        cache_line_size: int,
        clk_domain: ClockDomain,
    ):
        super().__init__(ruby_system.network, cache_line_size)

        self.cache = RubyCache(
            size=size, assoc=associativity, start_index_bit=self.getBlockSizeBits(),
            ruby_system=ruby_system
        )
        self.ruby_system = ruby_system

        self.clk_domain = clk_domain
        self.use_prefetcher = False  # >>> Should be true

        # Only used for L1 controllers
        self.send_evictions = False
        self.sequencer = NULL

        # Only applies to home nodes
        self.is_HN = False
        self.enable_DMT = False
        self.enable_DCT = False

        # Allow owned state
        self.allow_SD = True

        # Prevent forwarding since I have no idea whether it should be T/F
        self.fwd_unique_on_readshared = False

        ###########################
        # Don't apply to L2
        self.alloc_on_seq_acc = False
        self.alloc_on_seq_line_write = False
        ###########################

        ###########################
        # Keeping L2 inclusive of L1
        self.alloc_on_readshared = True
        self.alloc_on_readunique = True
        self.alloc_on_readonce = True
        self.dealloc_on_unique = False
        self.dealloc_on_shared = False
        self.dealloc_backinv_unique = True
        self.dealloc_backinv_shared = True
        self.alloc_on_writeback = False  # Shouldn't matter since inclusive
        ###########################

        # Some reasonable default TBE params
        self.number_of_TBEs = 16
        self.number_of_repl_TBEs = 16
        self.number_of_snoop_TBEs = 4
        self.number_of_DVM_TBEs = 16
        self.number_of_DVM_snoop_TBEs = 4
        self.unify_repl_TBEs = False