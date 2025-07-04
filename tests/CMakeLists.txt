cmake_minimum_required(VERSION 3.10)

project(tests)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

include_directories(include)
include_directories(packages)

file(GLOB_RECURSE SOURCES "src/*.cpp")

add_executable(tests ${SOURCES})




target_link_libraries(tests PRIVATE nlohmann_json::nlohmann_json)

add_subdirectory(packages/fmt-11.2.0)

target_link_libraries(tests PRIVATE fmt)

add_subdirectory(packages/spdlog-1.15.3)

target_link_libraries(tests PRIVATE spdlog)



add_subdirectory(packages/nlohmannjson-3.12.0)





add_subdirectory(packages/glm-1.0.1)

target_link_libraries(tests PRIVATE glm)
