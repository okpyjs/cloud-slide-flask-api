from typing import List


class PPTX:
    def __init__(self, result_file_name: str, file_list: list[str]) -> None:
        self.result_file_name = result_file_name
        self.file_list = file_list

    def convert(self):
        return "result_file_name"
