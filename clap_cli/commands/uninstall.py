import os
import json
import stat
import shutil
from commands.command import Command


def remove_readonly(func, path, _):
    os.chmod(path, stat.S_IWRITE)
    func(path)


class UninstallCommand(Command):
    def __init__(self):
        self.install_dir = "packages"
        self.manifest_file = "clap_package.json"
        self.cmake_file = "CMakeLists.txt"

    def run(self, args) -> None:
        package_name = args.name

        # Vérifie que le manifest existe
        if not os.path.exists(self.manifest_file):
            print("❌ Error: No clap_package.json found.")
            return
        
        # Change les données du manifeste
        with open(self.manifest_file, "r", encoding="utf-8") as f:
            manifest_data = json.load(f)

        version = manifest_data.get("dependencies", {}).get(package_name)
        if not version:
            print(f"⚠️ Package '{package_name}' not found in dependencies.")
            return
        
        # Supprime le dossier
        folder = os.path.join(self.install_dir, f"{package_name}-{version}")
        if os.path.isdir(folder):
            try:
                shutil.rmtree(folder, onexc=remove_readonly)
                print(f"🧹 Removed folder: {folder}")
            except PermissionError as e:
                print(f"❌ Cannot remove folder {folder}: {e}")
                print("➡️ Assurez-vous que le dossier n'est pas ouvert dans un éditeur ou utilisé par un processus (ex: VSCode, CMake, Explorer).")
                return
        else:
            print(f"⚠️ Package folder not found: {folder}")

        # Supprime du manifeste
        manifest_data["dependencies"].pop(package_name)
        with open(self.manifest_file, "w", encoding="utf-8") as f:
            json.dump(manifest_data, f, indent=4)
        print(f"📄 Updated {self.manifest_file} (removed {package_name})")

        # Nettoyage du CMakeLists.txt
        self._remove_from_cmake(package_name, version)

    def _remove_from_cmake(self, package_name: str, version: str) -> None:
        if not os.path.exists(self.cmake_file):
            return
        
        with open(self.cmake_file, "r", encoding="utf-8") as f:
            lines = f.readlines()

        projects_settings = self._get_project_settings()

        pkg_dir = f"add_subdirectory(packages/{package_name}-{version})"
        lib_line_prefix = f"target_link_libraries({projects_settings.get('name')} PRIVATE"

        new_lines = []
        skip_next_link_line = False
        for line in lines:
            if pkg_dir in line:
                skip_next_link_line = True
                continue
            if skip_next_link_line and lib_line_prefix in line and package_name in line:
                skip_next_link_line = False
                continue
            new_lines.append(line)

        with open(self.cmake_file, "w", encoding="utf-8") as f:
            f.writelines(new_lines)

        print(f"🛠️ Removed CMake entries for {package_name}-{version}")