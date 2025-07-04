import os
import sys
import json
import subprocess
import shlex
from commands.build import BuildCommand


class RunCommand(BuildCommand):
    def __init__(self):
        super().__init__()

    def run(self, args) -> None:
        super().run(args)
        project_settings = self._get_project_settings()
        
        # Récupération du nom du binaire
        executable_name = project_settings.get("name")
        if sys.platform.startswith("win"):
            executable_name += ".exe"
        executable_path = os.path.join(self.build_dir, executable_name)

        if not os.path.exists(executable_path):
            print(f"❌ Executable '{executable_name}' not found after build.")
            return
        
        # Exécution du binaire
        print(f"🚀 Running ./{executable_name}...")
        print("\n--------------------------------------------------------------------------------\n")
        subprocess.run([f"./{executable_path}"], cwd=self.build_dir)
