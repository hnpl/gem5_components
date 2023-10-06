from gem5.components.cachehierarchies.chi.nodes.abstract_node import AbstractNode

from m5.objects import NULL, RubyCache

class L3Slice(AbstractNode):
    def __init__(self, size, associativity, ruby_system, cache_line_size, clk_domain):
        super().__init__(ruby_system.network, cache_line_size)
        self.cache = RubyCache(size=size, assoc=associativity, start_index_bit=self.getBlockSizeBits())
        self.clk_domain = clk_domain
        self.use_prefetcher = False
        self.ruby_system = ruby_system

        # From CMN
        # Only used for L1 controllers
        self.send_evictions = False
        self.sequencer = NULL

        self.is_HN = True
        self.enable_DMT = True
        self.enable_DCT = True

        self.allow_SD = True

        self.alloc_on_seq_acc = False  # Does not apply to L3
        self.alloc_on_seq_line_write = False

        self.alloc_on_readshared = (
            False  # I think this should be True for perf
        )
        self.alloc_on_readunique = False
        self.alloc_on_readonce = False

        # insert on writeback (victim cache)
        self.alloc_on_writeback = True

        # Keep the line if a requestor asks for unique/shared
        ###########################
        self.dealloc_on_unique = False
        self.dealloc_on_shared = False
        ###########################

        # Allow caches closer to core to keep block even if evicted from L3
        self.dealloc_backinv_unique = False
        self.dealloc_backinv_shared = False

        # Some reasonable default TBE params
        self.number_of_TBEs = 128
        self.number_of_repl_TBEs = 128
        self.number_of_snoop_TBEs = 4
        self.number_of_DVM_TBEs = 16
        self.number_of_DVM_snoop_TBEs = 4
        self.unify_repl_TBEs = False