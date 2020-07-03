project(metal.test)

cmake_minimum_required(VERSION 3.8)

add_library(serial src/metal/serial/syscalls.c)

include_directories(include)

add_subdirectory(test)