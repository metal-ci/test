add_executable(newlib_gdb newlib_gdb.c ${CMAKE_SOURCE_DIR}/src/metal/gdb/syscalls.c)
set_target_properties(newlib_gdb   PROPERTIES COMPILE_FLAGS "-g1 -ggdb -fno-omit-frame-pointer")

configure_file(newlib_gdb.gdbinit ${CMAKE_CURRENT_BINARY_DIR}/newlib_gdb.gdbinit)

add_test(newlib_gdb
        COMMAND PYTHONPATH=$PYTHONPATH:${PROJECT_SOURCE_DIR}
        gdb --command=${CMAKE_CURRENT_BINARY_DIR}/newlib_gdb.gdbinit $<TARGET_FILE:newlib_gdb> ${CMAKE_CURRENT_BINARY_DIR}/newlib_gdb.gdbinit
        WORKING_DIRECTORY ${PROJECT_SOURCE_DIR})