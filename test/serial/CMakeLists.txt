enable_testing()

add_executable(read_test read.c)
add_executable(write_test write.c)
add_executable(newlib_blocked newlib_blocked.c ${CMAKE_SOURCE_DIR}/src/metal/serial/syscalls.c)
target_compile_definitions(newlib_blocked PUBLIC -DMETAL_SERIAL_SYSCALLS_MODE=METAL_SERIAL_SYSCALLS_MODE_BLOCKED)


get_target_property(LIBA_INCLUDES read_test INCLUDE_DIRECTORIES)
message("Including ${LIBA_INCLUDES}, ${CMAKE_C_IMPLICIT_INCLUDE_DIRECTORIES}, ${CMAKE_CXX_IMPLICIT_INCLUDE_DIRECTORIES}")


add_test(NAME read_test COMMAND ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/read_test_runner.py
        $<TARGET_FILE:read_test> --include=${PROJECT_SOURCE_DIR}/include
        WORKING_DIRECTORY ${PROJECT_SOURCE_DIR})

add_test(NAME write_test COMMAND ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/write_test_runner.py
        $<TARGET_FILE:write_test> --include=${PROJECT_SOURCE_DIR}/include
        WORKING_DIRECTORY ${PROJECT_SOURCE_DIR})

#set_target_properties(serial_compile_test_c   PROPERTIES COMPILE_FLAGS "-g -gdwarf-4 -Og -fno-omit-frame-pointer")
#set_target_properties(serial_compile_test_cpp PROPERTIES COMPILE_FLAGS "-g -gdwarf-4 -Og -fno-omit-frame-pointer")