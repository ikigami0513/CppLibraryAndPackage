import os
import sys
import json
import subprocess
import shlex
from commands.command import Command


class BuildCommand(Command):
    def __init__(self):
        self.build_dir = "build"
        self.cmake_file = "CMakeLists.txt"

    def run(self, args) -> None:
        # Vérifie que le projet est bien initialisé
        if not os.path.exists(self.cmake_file):
            print("❌ Error: CMakeLists.txt not found. Make sure you're in a Clap project.")
            return
        
        os.makedirs(self.build_dir, exist_ok=True)

        # Etape de génération CMake
        project_settings = self._get_project_settings()

        print("🔧 Running CMake...")
        result = subprocess.run(
            shlex.split(project_settings.get("cmake", "")),
            cwd=self.build_dir
        )
        if result.returncode != 0:
            print("❌ CMake configuration failed:")
            print(result.stderr)
            return
        
        # Etape de compilation
        print("⚙️ Building project...")
        result = subprocess.run(
            shlex.split(project_settings.get("make", "")),
            cwd=self.build_dir
        )
        if result.returncode != 0:
            print("❌ Build failed:")
            print(result.stderr)
            return
