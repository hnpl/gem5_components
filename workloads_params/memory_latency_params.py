from .isa_extensions import ISAExtension
from .params import Params
from .isa import ISA

from pathlib import Path
from typing import List

class MemoryLatencyTestParams(Params):
    def __init__(self, source_path: Path, with_roi_annotations: bool, isa: ISA, isa_extensions: List[ISAExtension] = []) -> None:
        super().__init__(source_path, with_roi_annotations, isa_extensions)
        if with_roi_annotations:
            assert(False and "MemoryLatencyTest does not have the ROI-annotated variant.")
        self.isa = isa

    def get_command(self) -> str:
        binary_suffix = "unknown"
        if self.isa == ISA.ARM:
            binary_suffix = "aarch64"
        elif self.isa == ISA.RISCV:
            binary_suffix = "riscv64"
        else:
            assert(False and "Unsupported ISA")
        binary_name = "memorylatency-" + binary_suffix
        path = self.source_path / "build" / "src" / binary_name
        return str(path)

    def get_naming_string(self) -> str:
        return "memory-latency-test"
