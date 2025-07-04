import json
from abc import ABC


class Command(ABC):
    def _get_project_settings(self) -> str:
        try:
            with open("clap_package.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                return data
        except Exception:
            return {}
        
    def run(self, args): ...
    