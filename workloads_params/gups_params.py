from params import Params

from gem5.utils.override import overrides

from pathlib import Path

def isPowerOf2(n):
    return (n & (n - 1)) == 0

class GUPSParams(Params):
    def __init__(self, source_path: Path, with_roi_annotation: bool, table_number_of_elements: int, number_of_updates_inner_loop: int) -> None:
        super().__init__(source_path, with_roi_annotation)
        assert(isPowerOf2(table_number_of_elements))
        assert(isPowerOf2(number_of_updates_inner_loop))
        self.table_number_of_elements = table_number_of_elements
        self.number_of_updates_inner_loop = number_of_updates_inner_loop

    @overrides(Params)
    def get_command(self) -> str:
        binary_name = "gups.hw.m5" if self.with_roi_annotation else "gups.hw"
        path = source_path / binary_name
        return f"{str(path)} {self.table_number_of_elements} {self.number_of_updates_inner_loop}"

    @overrides(Params)
    def get_naming_string(self) -> str:
        return "-".join(["gups", str(self.table_number_of_elements), str(self.number_of_updates_inner_loop)])
