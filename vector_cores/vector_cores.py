from abc import abstractmethod
from typing import Union

from gem5.utils.requires import requires
from gem5.utils.override import overrides

from gem5.components.boards.abstract_board import AbstractBoard
from gem5.components.boards.mem_mode import MemMode
from gem5.components.processors.base_cpu_processor import BaseCPUProcessor
from gem5.components.processors.simple_core import SimpleCore
from gem5.components.processors.switchable_processor import SwitchableProcessor
from gem5.components.processors.cpu_types import CPUTypes, get_mem_mode
from gem5.isas import ISA

from m5.objects import BaseISA
from m5.util import warn

class BaseVectorParameters:
    def __init__(self):
        pass
    def apply(self, core: SimpleCore):
        self._apply_isa_change(core.isa)
        self._apply_isa_change(core.decoder[0].isa)
    @abstractmethod
    def _apply_isa_change(self, isa_object: BaseISA):
        pass

class ARM_SVE_Parameters(BaseVectorParameters):
    def __init__(self, sve_vl):
        self.sve_vl = sve_vl
        requires((sve_vl % 128 == 0) and (sve_vl > 0) and (sve_vl <= 2048))
    @overrides(BaseVectorParameters)
    def _apply_isa_change(self, isa_object: BaseISA):
        isa_object.sve_vl = self.sve_vl

class RVV_Parameters(BaseVectorParameters):
    def __init__(self, elen, vlen):
        self.elen = elen
        self.vlen = vlen
    @overrides(BaseVectorParameters)
    def _apply_isa_change(self, isa_object: BaseISA):
        from pprint import pprint
        pprint(vars(isa_object[0]))
        isa_object[0].elen = self.elen
        isa_object[0].vlen = self.vlen

class SimpleVectorCore(SimpleCore):
    def __init__(self, cpu_type: CPUTypes, core_id: int, isa: ISA,
            isa_vector_parameters: BaseVectorParameters):
        super().__init__(cpu_type, core_id, isa)
        from pprint import pprint
        #pprint(vars(self.core))
        isa_vector_parameters.apply(self.core)

class SimpleVectorProcessor(BaseCPUProcessor):
    def __init__(self, cpu_type: CPUTypes, num_cores: int, isa: ISA,
                 isa_vector_parameters: BaseVectorParameters):
        super().__init__(cores=[
            SimpleVectorCore(cpu_type, core_id, isa, isa_vector_parameters)
            for core_id in range(num_cores)
        ])

class SimpleSwitchableVectorProcessor(SwitchableProcessor):
    def __init__(
        self,
        starting_core_type: CPUTypes,
        switch_core_type: CPUTypes,
        num_cores: int,
        isa: ISA,
        isa_vector_parameters: BaseVectorParameters
    ) -> None:
        if num_cores <= 0:
            raise AssertionError("Number of cores must be a positive integer!")
        self._start_key = "start"
        self._switch_key = "switch"
        self._current_is_start = True
        self._mem_mode = get_mem_mode(starting_core_type)
        switchable_cores = {
            self._start_key: [
                SimpleVectorCore(cpu_type=starting_core_type, core_id=i, isa=isa,
                                 isa_vector_parameters=isa_vector_parameters)
                for i in range(num_cores)
            ],
            self._switch_key: [
                SimpleVectorCore(cpu_type=switch_core_type, core_id=i, isa=isa,
                                 isa_vector_parameters=isa_vector_parameters)
                for i in range(num_cores)
            ],
        }
        super().__init__(
            switchable_cores=switchable_cores, starting_cores=self._start_key
        )

    @overrides(SwitchableProcessor)
    def incorporate_processor(self, board: AbstractBoard) -> None:
        super().incorporate_processor(board=board)
        if (
            board.get_cache_hierarchy().is_ruby()
            and self._mem_mode == MemMode.ATOMIC
        ):
            warn(
                "Using an atomic core with Ruby will result in "
                "'atomic_noncaching' memory mode. This will skip caching "
                "completely."
            )
            self._mem_mode = MemMode.ATOMIC_NONCACHING
        board.set_mem_mode(self._mem_mode)
    def switch(self):
        """Switches to the "switched out" cores."""
        if self._current_is_start:
            self.switch_to_processor(self._switch_key)
        else:
            self.switch_to_processor(self._start_key)
        self._current_is_start = not self._current_is_start
