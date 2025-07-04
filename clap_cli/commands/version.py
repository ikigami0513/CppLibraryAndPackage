from __version__ import __version__
from commands.command import Command


class VersionCommand(Command):
    def run(self, args) -> None:
        print(f"Clap version {__version__}")
        