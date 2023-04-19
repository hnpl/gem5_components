from abc import abstractmethod
from pathlib import Path
from typing import List

from .isa_extensions import ISAExtension

class Params:
    def __init__(self, source_path: Path, with_roi_annotations: bool, isa_extensions: List[ISAExtension]):
        assert(isinstance(source_path, Path))
        self.source_path = source_path
        self.with_roi_annotations = with_roi_annotations
        self.isa_extensions = sorted(isa_extensions)
    
    @abstractmethod
    def get_command(self) -> str:
        pass
    
    @abstractmethod
    def get_naming_string(self) -> str:
        pass
