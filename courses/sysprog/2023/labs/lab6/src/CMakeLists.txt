cmake_minimum_required(VERSION 3.20)
project(src C)

set(CMAKE_C_STANDARD 99)

# Register Zydis dependency.
# Disable build of tools and examples.
option(ZYDIS_BUILD_TOOLS "" OFF)
option(ZYDIS_BUILD_EXAMPLES "" OFF)
add_subdirectory("zydis")

add_executable(src ast.c cmdFuncs.c main.c)

# Have CMake link our project executable against Zydis.
target_link_libraries(src Zydis)