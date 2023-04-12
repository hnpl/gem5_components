from abc import abstractmethod

class Params:
    def __init__(self, source_path: str, with_roi_annotations: bool):
        self.source_path = source_path
        self.with_roi_annotations = with_roi_annotations
    
    @abstractmethod
    def get_command(self) -> str:
        pass
    
    @abstractmethod
    def get_naming_string(self) -> str:
        pass
