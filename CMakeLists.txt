project(metal.test)

cmake_minimum_required(VERSION 3.8)

add_library(serial_syscalls src/metal/serial/syscalls.c)
add_library(break_syscalls  src/metal/gdb/syscalls.c)

include_directories(include)

enable_testing()
add_subdirectory(test)