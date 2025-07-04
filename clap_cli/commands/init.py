import os
import json
from commands.command import Command


class InitCommand(Command):
    def __init__(self):
        self.filename = "clap_package.json"
        self.packages_dir = "packages"
        self.include_dir = "include"
        self.src_dir = "src"
        self.main_cpp_path = os.path.join(self.src_dir, "main.cpp")
        self.cmake_file = "CMakeLists.txt"

    def run(self, args) -> None:
        project_name = args.name.strip() if args.name else "clap_project"

        if os.path.exists(self.filename):
            print(f"⚠️  A Clap project already exists here (found {self.filename}).")
            return
        
        manifest_data = {
            "name": project_name,
            "cmake": "cmake ..",
            "make": "make",
            "dependencies": {}
        }

        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(manifest_data, f, indent=4)

        # Création des dossiers
        os.makedirs(self.packages_dir, exist_ok=True)
        os.makedirs(self.include_dir, exist_ok=True)
        os.makedirs(self.src_dir, exist_ok=True)

        # Fichier main.cpp par défaut
        default_main = """#include <iostream>

int main() {
    std::cout << "Hello from Clap project!" << std::endl;
    return 0;
}
"""

        with open(self.main_cpp_path, "w", encoding="utf-8") as f:
            f.write(default_main)

        # Fichier CMakeLists.txt par défaut
        cmake_template = f"""cmake_minimum_required(VERSION 3.10)

project({project_name})

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

include_directories(include)
include_directories(packages)

file(GLOB_RECURSE SOURCES "src/*.cpp")

add_executable({project_name} ${{SOURCES}})
"""
        
        with open(self.cmake_file, "w", encoding="utf-8") as f:
            f.write(cmake_template)

        # Affichage
        print(f"✅ Initialized Clap project '{project_name}'")
        print(f"📦 Created {self.filename} and {self.packages_dir}/ directory.")
        print(f"📁 Directories: {self.packages_dir}/, {self.include_dir}/, {self.src_dir}/")
