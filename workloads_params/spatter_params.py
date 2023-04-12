from params import Params

from gem5.utils.override import overrides

from pathlib import Path

class SpatterParams(Params):
    def __init__(self, source_path: Path, with_roi_annotation: bool, json_filepath: str) -> None:
        super().__init__(source_path, with_roi_annotation)
        self.json_filepath = json_filepath

    @overrides(Params)
    def get_command(self) -> str:
        binary_name = "spatter.hw.m5" if self.with_roi_annotation else "spatter.hw"
        path = source_path / binary_name
        return f"{str(path)} {self.json_filepath}"

    @overrides(Params)
    def get_naming_string(self) -> str:
        return "-".join(["spatter", Path(self.json_file_path).name])
