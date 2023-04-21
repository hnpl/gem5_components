from .isa_extensions import ISAExtension
from .params import Params

from pathlib import Path
from typing import List

class GUPSParams(Params):
    def __init__(self, source_path: Path, with_roi_annotations: bool, seed: int, mod: int, isa_extensions: List[ISAExtension] = []) -> None:
        super().__init__(source_path, with_roi_annotations, isa_extensions)
        self.seed = seed
        self.mod = mod

    def get_command(self) -> str:
        binary_name = ["permutating_gather", "hw"]
        if self.isa_extensions:
            binary_name.extend(self.isa_extensions)
        if self.with_roi_annotations:
            binary_name.append("m5")
        binary_name = ".".join(binary_name)
        path = self.source_path / binary_name
        return f"{str(path)} {self.seed} {self.mod}"

    def get_naming_string(self) -> str:
        return "-".join(["permutating_gather", str(self.seed), str(self.mod)])
