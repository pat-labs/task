import json
import os

class MyFileSystem:
    file_extension = ".json"

    def __init__(self, path: str):
        self.path = path

    def write(self, json_data: dict):
        with open(self.path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)

    def read(self) -> dict:
        if not os.path.exists(self.path):
            return {}
        with open(self.path, 'r', encoding='utf-8') as f:
            return json.load(f)
