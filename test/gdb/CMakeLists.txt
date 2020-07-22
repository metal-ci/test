add_executable(newlib_gdb newlib_gdb.c ${CMAKE_SOURCE_DIR}/src/metal/gdb/syscalls.c)
set_target_properties(newlib_gdb   PROPERTIES COMPILE_FLAGS "-g1 -ggdb -fno-omit-frame-pointer")

configure_file(newlib_gdb.gdbinit ${CMAKE_CURRENT_BINARY_DIR}/newlib_gdb.gdbinit)

add_test(NAME newlib_gdb
        COMMAND gdb --command=${CMAKE_CURRENT_BINARY_DIR}/newlib_gdb.gdbinit $<TARGET_FILE:newlib_gdb> ${CMAKE_CURRENT_BINARY_DIR}/newlib_gdb.gdbinit
        WORKING_DIRECTORY ${PROJECT_SOURCE_DIR})


add_executable(argv_gdb argv_gdb.c)
set_target_properties(argv_gdb   PROPERTIES COMPILE_FLAGS "-g1 -ggdb -fno-omit-frame-pointer")

configure_file(argv_gdb.gdbinit ${CMAKE_CURRENT_BINARY_DIR}/argv_gdb.gdbinit)

add_test(NAME argv_gdb
        COMMAND  gdb --command=${CMAKE_CURRENT_BINARY_DIR}/argv_gdb.gdbinit $<TARGET_FILE:argv_gdb> ${CMAKE_CURRENT_BINARY_DIR}/argv_gdb.gdbinit
        WORKING_DIRECTORY ${PROJECT_SOURCE_DIR})


add_executable(unit_gdb unit_gdb.c)
configure_file(unit_gdb.gdbinit ${CMAKE_CURRENT_BINARY_DIR}/unit_gdb.gdbinit)
set_target_properties(unit_gdb   PROPERTIES COMPILE_FLAGS "-g1 -ggdb -fno-omit-frame-pointer")

add_test(NAME unit_gdb
        COMMAND gdb --command=${CMAKE_CURRENT_BINARY_DIR}/unit_gdb.gdbinit $<TARGET_FILE:unit_gdb> ${CMAKE_CURRENT_BINARY_DIR}/unit_gdb.gdbinit
        WORKING_DIRECTORY ${PROJECT_SOURCE_DIR})


add_executable(catch_gdb catch_gdb.cpp)
configure_file(catch_gdb.gdbinit ${CMAKE_CURRENT_BINARY_DIR}/catch_gdb.gdbinit)
set_target_properties(catch_gdb   PROPERTIES COMPILE_FLAGS "-g1 -ggdb -fno-omit-frame-pointer")

add_test(NAME catch_gdb
        COMMAND  gdb --command=${CMAKE_CURRENT_BINARY_DIR}/catch_gdb.gdbinit $<TARGET_FILE:catch_gdb> ${CMAKE_CURRENT_BINARY_DIR}/catch_gdb.gdbinit
        WORKING_DIRECTORY ${PROJECT_SOURCE_DIR})

set_tests_properties(newlib_gdb argv_gdb unit_gdb catch_gdb PROPERTIES ENVIRONMENT PYTHONPATH=$PYTHONPATH:${PROJECT_SOURCE_DIR})