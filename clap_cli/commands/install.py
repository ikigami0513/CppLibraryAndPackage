import os
import re
import json
import shutil
from client import ClapClient
from commands.command import Command
from utils.zip_utils import extract_zip_file
from typing import Dict, Optional


class InstallCommand(Command):
    def __init__(self):
        self.client = ClapClient()
        self.install_dir = "packages"
        self.manifest_file = "clap_package.json"
        self.cmake_file = "CMakeLists.txt"

    def run(self, args) -> None:
        # 🔒 Vérifie si le projet a été initialisé
        if not os.path.exists(self.manifest_file):
            print("❌ Error: Clap project not initialized. Please run `clap init --name <project>` first.")
            return
        
        if not args.name:
            # Mode "install all"

            project_settings = self._get_project_settings()
            dependencies: Dict[str, str] = project_settings.get("dependencies", {})
            if not dependencies:
                print("ℹ️ No dependencies to install.")
                return 

            for name, version in dependencies.items():
                install_path = os.path.join(self.install_dir, f"{name}-{version}")
                if os.path.exists(install_path):
                    print(f"✅ {name} {version} already installed.")
                    continue
                self._install_package(name, version)

        else:
            self._install_package(args.name, args.version)
        
    def _install_package(self, name: str, version: Optional[str] = None) -> None:
        response = self.client.info_package(name=name, version=version)
        package_name = response.get("name")
        package_version = response.get("version")
        package_target_library = response.get("target_library")
        response_file = self.client.download_package(package_name, version=package_version)

        # Récupère le nom du fichier zip
        content_disposition = response_file.headers.get('Content-Disposition', '')
        filename = self._extract_filename(content_disposition) or f"{name}.zip"

        # Chemin du fichier
        os.makedirs(self.install_dir, exist_ok=True)
        zip_path = os.path.join(self.install_dir, filename)

        with open(zip_path, "wb") as f:
            f.write(response_file.content)
        print(f"✅ Downloaded: {filename}")

        # Extraction
        extract_path = os.path.join(self.install_dir, filename.replace(".zip", ""))
        extract_zip_file(zip_path, extract_path)
        inner_path = os.path.join(extract_path, os.path.basename(extract_path))
        if os.path.isdir(inner_path):
            # Déplace tout son contenu un niveau au-dessus
            for item in os.listdir(inner_path):
                shutil.move(os.path.join(inner_path, item), extract_path)
            # Supprime le dossier redondant
            os.rmdir(inner_path)
        print(f"📦 Extracted to: {extract_path}")

        # Suppression du zip
        try:
            os.remove(zip_path)
            print(f"🧹 Removed zip file: {zip_path}")
        except OSError as e:
            print(f"⚠️ Failed to remove zip file: {e}")

        # Mise à jour du manifest
        self._update_manifest(package_name, package_version)
        self._update_cmake_file(f"{package_name}-{package_version}")
        project_settings = self._get_project_settings()
        self._link_package_in_cmake(project_settings.get("name", ""), package_target_library)

    def _extract_filename(self, content_disposition: str) -> str | None:
        match = re.search(r'filename="([^"]+)"', content_disposition)
        return match.group(1) if match else None

    def _extract_version_from_filename(self, filename: str) -> str:
        match = re.match(r"(.+)-([0-9a-zA-Z_.\-]+)\.zip", filename)
        return match.group(2) if match else "unknown"

    def _update_manifest(self, name: str, version: str) -> None:
        with open(self.manifest_file, "r", encoding="utf-8") as f:
            manifest_data = json.load(f)

        manifest_data.setdefault("dependencies", {})[name] = version

        with open(self.manifest_file, "w", encoding="utf-8") as f:
            json.dump(manifest_data, f, indent=4)

        print(f"📄 Updated {self.manifest_file} with {name} = {version}")

    def _update_cmake_file(self, package_name: str) -> None:
        if not os.path.exists(self.cmake_file):
            print("⚠️ Warning: CMakeLists.txt not found. Skipping CMake update.")
            return
        
        line_to_add = f"add_subdirectory({self.install_dir}/{package_name})"

        with open(self.cmake_file, "r", encoding="utf-8") as f:
            content = f.read()

        if line_to_add in content:
            print(f"ℹ️ {line_to_add} already present in {self.cmake_file}.")
            return
        
        with open(self.cmake_file, "a", encoding="utf-8") as f:
            f.write("\n" + line_to_add + "\n")

        print(f"🛠️ Updated {self.cmake_file} with: {line_to_add}")

    def _link_package_in_cmake(self, project_name: str, package_name: str) -> None:
        if not os.path.exists(self.cmake_file):
            print("⚠️ Warning: CMakeLists.txt not found. Skipping target_link_libraries.")
            return

        link_line = f"target_link_libraries({project_name} PRIVATE {package_name})"

        with open(self.cmake_file, "r", encoding="utf-8") as f:
            content = f.read()

        if link_line in content:
            print(f"ℹ️ Link already present in {self.cmake_file}.")
            return

        with open(self.cmake_file, "a", encoding="utf-8") as f:
            f.write("\n" + link_line + "\n")

        print(f"🔗 Linked {package_name} to {project_name} in {self.cmake_file}")
