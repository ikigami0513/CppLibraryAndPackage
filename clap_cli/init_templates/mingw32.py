from init_templates.template import Template


class Mingw32(Template):
    def cmake(self) -> str:
        return "cmake .. -G \"MinGW Makefiles\" -DCMAKE_C_COMPILER=gcc -DCMAKE_CXX_COMPILER=g++"
    
    def make(self) -> str:
        return "mingw32-make.exe"
    
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