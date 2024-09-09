cmake_minimum_required(VERSION 3.18)
project(concurStack C)

set(CMAKE_C_STANDARD 99)
add_executable(concurStack main.c cas.c spinlock.c stack.c )
find_package(Threads REQUIRED)
target_link_libraries(concurStack Threads::Threads)


