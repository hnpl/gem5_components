from .isa_extensions import ISAExtension
from .params import Params

from pathlib import Path
from typing import List

def isPowerOf2(n):
    return (n & (n - 1)) == 0

class GUPSParams(Params):
    def __init__(self, source_path: Path, with_roi_annotations: bool, table_number_of_elements: int, number_of_updates_inner_loop: int, isa_extensions: List[ISAExtension] = []) -> None:
        super().__init__(source_path, with_roi_annotations, isa_extensions)
        assert(isPowerOf2(table_number_of_elements))
        assert(isPowerOf2(number_of_updates_inner_loop))
        self.table_number_of_elements = table_number_of_elements
        self.number_of_updates_inner_loop = number_of_updates_inner_loop

    def get_command(self) -> str:
        binary_name = ["gups", "hw"]
        if self.isa_extensions:
            binary_name.extend(self.isa_extensions)
        if self.with_roi_annotations:
            binary_name.append("m5")
        binary_name = ".".join(binary_name)
        path = self.source_path / binary_name
        return f"{str(path)} {self.table_number_of_elements} {self.number_of_updates_inner_loop}"

    def get_naming_string(self) -> str:
        return "-".join(["gups", str(self.table_number_of_elements), str(self.number_of_updates_inner_loop)])
