from .params import Params

from pathlib import Path

class STREAMParams(Params):
    def __init__(self, source_path: Path, with_roi_annotations: bool, number_of_elements: int) -> None:
        super().__init__(source_path, with_roi_annotations)
        self.number_of_elements = number_of_elements

    def get_command(self) -> str:
        binary_name = "stream.hw.m5" if self.with_roi_annotations else "stream.hw"
        path = source_path / binary_name
        return f"{str(path)} {str(self.number_of_elements)}"

    def get_naming_string(self) -> str:
        return "-".join(["stream", str(self.number_of_elements)])
