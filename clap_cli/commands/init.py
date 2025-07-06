import os
import json
from commands.command import Command
from typing import Dict, Type

from init_templates.template import Template
from init_templates.cmake import CmakeTemplate
from init_templates.mingw32 import Mingw32


class InitCommand(Command):
    templates: Dict[str, Type[Template]] = {
        "cmake": CmakeTemplate,
        "mingw32": Mingw32
    }

    def __init__(self):
        self.filename = "clap_package.json"
        self.packages_dir = "packages"
        self.include_dir = "include"
        self.src_dir = "src"
        self.main_cpp_path = os.path.join(self.src_dir, "main.cpp")
        self.cmake_file = "CMakeLists.txt"

    def run(self, args) -> None:
        project_name = args.name.strip() if args.name else "clap_project"

        template_name = args.template
        if template_name is None:
            template_name = "cmake"

        template_cls = InitCommand.templates.get(template_name)
        if template_cls is None:
            print(f"Template {template_name} not found.")
            return
        
        template = template_cls()

        if os.path.exists(self.filename):
            print(f"⚠️  A Clap project already exists here (found {self.filename}).")
            return
        
        manifest_data = {
            "name": project_name,
            "cmake": template.cmake(),
            "make": template.make(),
            "dependencies": {}
        }

        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(manifest_data, f, indent=4)

        # Création des dossiers
        os.makedirs(self.packages_dir, exist_ok=True)
        os.makedirs(self.include_dir, exist_ok=True)
        os.makedirs(self.src_dir, exist_ok=True)

        with open(self.main_cpp_path, "w", encoding="utf-8") as f:
            f.write(template.main())
        
        with open(self.cmake_file, "w", encoding="utf-8") as f:
            f.write(template.cmakelists(project_name))

        # Affichage
        print(f"✅ Initialized Clap project '{project_name}'")
        print(f"📦 Created {self.filename} and {self.packages_dir}/ directory.")
        print(f"📁 Directories: {self.packages_dir}/, {self.include_dir}/, {self.src_dir}/")
