from init_templates.template import Template


class CmakeTemplate(Template):
    def cmake(self) -> str:
        return "cmake .."
    
    def make(self) -> str:
        return "make"
    
    def main(self) -> str:
        return """#include <iostream>

int main() {
    std::cout << "Hello from Clap project!" << std::endl;
    return 0;
}
"""

    def cmakelists(self, project_name: str) -> str:
        return f"""cmake_minimum_required(VERSION 3.10)

project({project_name})

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

include_directories(include)
include_directories(packages)

file(GLOB_RECURSE SOURCES "src/*.cpp")

add_executable({project_name} ${{SOURCES}})
"""
    