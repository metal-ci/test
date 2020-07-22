enable_testing()
find_package (Python COMPONENTS Interpreter)

add_subdirectory(gdb)
add_subdirectory(serial)
add_subdirectory(hosted)

