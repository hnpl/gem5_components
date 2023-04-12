from abc import abstractmethod
from pathlib import Path

class Params:
    def __init__(self, source_path: Path, with_roi_annotations: bool):
        assert(isinstance(source_path, Path))
        self.source_path = source_path
        self.with_roi_annotations = with_roi_annotations
    
    @abstractmethod
    def get_command(self) -> str:
        pass
    
    @abstractmethod
    def get_naming_string(self) -> str:
        pass
