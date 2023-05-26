from .isa_extensions import ISAExtension
from .params import Params

from pathlib import Path
from typing import List

class MemoryLatencyTestParams(Params):
    def __init__(self, source_path: Path, with_roi_annotations: bool, isa_extensions: List[ISAExtension] = []) -> None:
        super().__init__(source_path, with_roi_annotations, isa_extensions)

    def get_command(self) -> str:
        binary_name = "memorylatency"
        if self.with_roi_annotations:
            binary_name += ".m5"
        path = self.source_path / "build" / "src" / binary_name
        return str(path)

    def get_naming_string(self) -> str:
        return "memory-latency-test"
