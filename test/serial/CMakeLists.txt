enable_testing()

add_executable(read_test read.c)
add_executable(write_test write.c)
add_executable(cprint_test cio.c)


add_test(NAME read_test COMMAND ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/read_test_runner.py
        --binary=$<TARGET_FILE:read_test> --source-dir=${CMAKE_SOURCE_DIR}
        --bin-dir=${CMAKE_CURRENT_BINARY_DIR} WORKING_DIRECTORY ${PROJECT_SOURCE_DIR})

add_test(NAME write_test COMMAND ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/write_test_runner.py
        --binary=$<TARGET_FILE:write_test> --source-dir=${CMAKE_SOURCE_DIR}
        --bin-dir=${CMAKE_CURRENT_BINARY_DIR} WORKING_DIRECTORY ${PROJECT_SOURCE_DIR})

#set_target_properties(serial_compile_test_c   PROPERTIES COMPILE_FLAGS "-g -gdwarf-4 -Og -fno-omit-frame-pointer")
#set_target_properties(serial_compile_test_cpp PROPERTIES COMPILE_FLAGS "-g -gdwarf-4 -Og -fno-omit-frame-pointer")