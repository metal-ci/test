project(metal.test)

cmake_minimum_required(VERSION 3.8)

add_library(serial_syscalls src/metal/serial/syscalls.c)
add_library(gdb_syscalls  src/metal/gdb/syscalls.c)

add_library(serial_cpputest src/metal/serial/cpputest.cpp)
add_library(gdb_cpputest  src/metal/gdb/cpputest.cpp)

include_directories(libs/cpputest/include include)

add_subdirectory(libs/cpputest)
add_subdirectory(test)

