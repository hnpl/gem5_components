from .isa_extensions import ISAExtension
from .params import Params

from pathlib import Path
from typing import List

class STREAMParams(Params):
    def __init__(self, source_path: Path, with_roi_annotations: bool, number_of_elements: int, isa_extensions: List[ISAExtension] = []) -> None:
        super().__init__(source_path, with_roi_annotations, isa_extensions)
        self.number_of_elements = number_of_elements

    def get_command(self) -> str:
        binary_name = ["stream", "hw"]
        if self.isa_extensions:
            binary_name.extend(self.isa_extensions)
        if self.with_roi_annotations:
            binary_name.append("m5")
        binary_name = ".".join(binary_name)
        path = self.source_path / binary_name
        return f"{path} {self.number_of_elements}"

    def get_naming_string(self) -> str:
        return "-".join(["stream", str(self.number_of_elements)])
