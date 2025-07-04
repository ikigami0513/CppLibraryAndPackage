import argparse
import sys
from __version__ import __version__
from commands.command import Command
from typing import Type, Dict

from commands.init import InitCommand
from commands.install import InstallCommand
from commands.uninstall import UninstallCommand
from commands.run import RunCommand
from commands.build import BuildCommand
from commands.list import ListCommand
from commands.version import VersionCommand


def main():
    parser = argparse.ArgumentParser(
        prog="clap",
        description="Clap package manager for C++"
    )

    # ✅ Ajout du flag global --version
    parser.add_argument('--version', action='store_true', help='Show the version of Clap and exit')

    # Sous-commandes
    subparsers = parser.add_subparsers(dest="command")

    init_parser = subparsers.add_parser("init", help="Initialize a project")
    init_parser.add_argument("name", type=str, help="Project name")

    install_parser = subparsers.add_parser("install", help="Install a package")
    install_parser.add_argument("name", type=str, nargs="?", help="Package name")
    install_parser.add_argument("--version", type=str, help="Specific version")

    uninstall_parser = subparsers.add_parser("uninstall", help="Uninstall a package")
    uninstall_parser.add_argument("name", type=str, help="Package name")

    build_parser = subparsers.add_parser("build", help="Build the project")
    run_parser = subparsers.add_parser("run", help="Build and run the project")
    list_parser = subparsers.add_parser("list", help="List all packages in the project")
    subparsers.add_parser("version", help="Show Clap version")

    args = parser.parse_args()

    # ✅ Si --version est présent globalement
    if args.version:
        print(f"Clap version {__version__}")
        sys.exit(0)

    commands: Dict[str, Type[Command]] = {
        "init": InitCommand,
        "install": InstallCommand,
        "uninstall": UninstallCommand,
        "build": BuildCommand,
        "run": RunCommand,
        "list": ListCommand,
        "version": VersionCommand
    }

    if args.command is None:
        parser.print_help()
        sys.exit(1)

    command = commands.get(args.command)
    if command:
        command().run(args)


if __name__ == "__main__":
    main()
