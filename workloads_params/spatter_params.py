from .params import Params

from pathlib import Path
from typing import List

class SpatterParams(Params):
    def __init__(self, source_path: Path, with_roi_annotations: bool, json_filepath: str, isa_extensions: List[ISAExtension] = []) -> None:
        super().__init__(source_path, with_roi_annotations, isa_extensions)
        self.json_filepath = json_filepath

    def get_command(self) -> str:
        binary_name = ["spatter", "hw"]
        if self.isa_extensions:
            binary_name.extend(isa_entensions)
        if self.with_roi_annotations:
            binary_name.append("m5")
        binary_name = ".".join(binary_name)
        path = self.source_path / binary_name
        return f"{str(path)} {self.json_filepath}"

    def get_naming_string(self) -> str:
        return "-".join(["spatter", Path(self.json_filepath).name])
