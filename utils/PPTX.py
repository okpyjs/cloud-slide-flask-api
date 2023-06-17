from typing import List


from Base import Base

class PPTX(Base):
    def __init__(self, result_file_name: str, file_list: list[str]) -> None:
        self.result_file_name = result_file_name
        self.file_list = file_list

    def convert(self):
        return "result_file_name"

    def merge(self, files: List[str]):
        return
