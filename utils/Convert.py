from .PPTX import PPTX
from .Slide import Slide


class Convert:
    def __init__(self, flag: str) -> None:
        if flag == "p":
            self.object = PPTX()
        
        if flag == "s":
            self.object = Slide()
