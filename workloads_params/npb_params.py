from .params import Params

from pathlib import Path

class NPBBenchmark:
    BT = "bt"
    CG = "cg"
    DC = "dc"
    EP = "ep"
    FT = "ft"
    IS = "is"
    LU = "lu"
    MG = "mg"
    SP = "sp"
    UA = "ua"

class NPBClass:
    S = "S"
    W = "W"
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"
    F = "F"

class NPBParams(Params):
    def __init__(self, source_path: Path, with_roi_annotations: bool, benchmark: NPBBenchmark, size: NPBClass) -> None:
        super().__init__(source_path, with_roi_annotations, isa_extensions = [])
        self.benchmark = benchmark
        self.size = size

    def get_command(self) -> str:
        path = self.source_path / "NPB3.4-OMP" / "bin" / f"{self.benchmark}.{self.size}.x"
        return str(path)

    def get_naming_string(self) -> str:
        return "-".join(["npb", self.benchmark, self.size])
