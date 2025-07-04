import json
from pathlib import Path
from commands.command import Command
from typing import Dict


class ListCommand(Command):
    def run(self, args):
        projects_settings = self._get_project_settings()

        deps: Dict[str, str] = projects_settings.get("dependencies", {})
        if not deps:
            print("No packages installed.")
            return
        
        print("Installed packages:")
        for name, version in deps.items():
            print(f"- {name} : {version}")
            