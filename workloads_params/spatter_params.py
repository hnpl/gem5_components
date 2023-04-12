from .params import Params

from pathlib import Path

class SpatterParams(Params):
    def __init__(self, source_path: Path, with_roi_annotations: bool, json_filepath: str) -> None:
        super().__init__(source_path, with_roi_annotations)
        self.json_filepath = json_filepath

    def get_command(self) -> str:
        binary_name = "spatter.hw.m5" if self.with_roi_annotations else "spatter.hw"
        path = self.source_path / binary_name
        return f"{str(path)} {self.json_filepath}"

    def get_naming_string(self) -> str:
        return "-".join(["spatter", Path(self.json_filepath).name])
