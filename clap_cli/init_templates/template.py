from abc import ABC


class Template:
    def cmake(self) -> str: ...

    def make(self) -> str: ...
    
    def main(self) -> str: ...

    def cmakelists(self) -> str: ...
    