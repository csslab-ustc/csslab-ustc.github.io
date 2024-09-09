cmake_minimum_required(VERSION 3.18)
project(shell C)

find_package(BISON)
find_package(FLEX)

set(CMAKE_C_STANDARD 99)

INCLUDE_DIRECTORIES(${CMAKE_CURRENT_BINARY_DIR})
INCLUDE_DIRECTORIES(${CMAKE_CURRENT_SOURCE_DIR})

FIND_LIBRARY(LEX_LIB l)

FLEX_TARGET(scanner scanner.l   ${CMAKE_CURRENT_BINARY_DIR}/lex.yy.c)
BISON_TARGET(parser parser.y    ${CMAKE_CURRENT_BINARY_DIR}/y.tab.c)

ADD_FLEX_BISON_DEPENDENCY(scanner parser)

ADD_EXECUTABLE(shell main.c ast.c ast.h
        ${BISON_parser_OUTPUTS}
        ${FLEX_scanner_OUTPUTS})
