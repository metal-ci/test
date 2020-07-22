
add_executable(read_test read.c)
add_executable(write_test write.c)
add_executable(newlib_blocked newlib_blocked.c ${CMAKE_SOURCE_DIR}/src/metal/serial/syscalls.c)

target_compile_definitions(newlib_blocked PUBLIC -DMETAL_SERIAL_SYSCALLS_MODE=METAL_SERIAL_SYSCALLS_MODE_BLOCKED)

add_executable(newlib_unchecked newlib_unchecked.c ${CMAKE_SOURCE_DIR}/src/metal/serial/syscalls.c)
target_compile_definitions(newlib_unchecked PUBLIC -DMETAL_SERIAL_SYSCALLS_MODE=METAL_SERIAL_SYSCALLS_MODE_UNCHECKED)

add_executable(newlib_full newlib_full.c ${CMAKE_SOURCE_DIR}/src/metal/serial/syscalls.c)
target_compile_definitions(newlib_full PUBLIC -DMETAL_SERIAL_SYSCALLS_MODE=METAL_SERIAL_SYSCALLS_MODE_FULL)

add_executable(argv_serial argv.c)

add_executable(unit_serial unit.c)
add_executable(catch_serial catch_serial.cpp)
#set_target_properties(unit_serial PROPERTIES COMPILE_FLAGS "-g -ggdb -Og -fno-stack-protector")

add_test(NAME read_test COMMAND ${Python_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/read_test_runner.py
        $<TARGET_FILE:read_test> --include=${PROJECT_SOURCE_DIR}/include --source-dir ${CMAKE_CURRENT_SOURCE_DIR}
        WORKING_DIRECTORY ${PROJECT_SOURCE_DIR})

add_test(NAME write_test COMMAND ${Python_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/write_test_runner.py
        $<TARGET_FILE:write_test> --include=${PROJECT_SOURCE_DIR}/include --source-dir ${CMAKE_CURRENT_SOURCE_DIR}
        WORKING_DIRECTORY ${PROJECT_SOURCE_DIR})

add_test(NAME newlib_blocked_test COMMAND ${Python_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/newlib_blocked.py
        $<TARGET_FILE:newlib_blocked> --include=${PROJECT_SOURCE_DIR}/include --source-dir ${CMAKE_CURRENT_SOURCE_DIR}
        WORKING_DIRECTORY ${PROJECT_SOURCE_DIR})


add_test(NAME newlib_unchecked_test COMMAND ${Python_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/newlib_unchecked.py
        $<TARGET_FILE:newlib_unchecked> --include=${PROJECT_SOURCE_DIR}/include --source-dir ${CMAKE_CURRENT_SOURCE_DIR}
        WORKING_DIRECTORY ${PROJECT_SOURCE_DIR})

add_test(NAME newlib_full_test COMMAND ${Python_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/newlib_full.py
        $<TARGET_FILE:newlib_full> --include=${PROJECT_SOURCE_DIR}/include --source-dir ${CMAKE_CURRENT_SOURCE_DIR}
        WORKING_DIRECTORY ${PROJECT_SOURCE_DIR})

add_test(NAME argv_test COMMAND ${Python_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/argv_runner.py
        $<TARGET_FILE:argv_serial> --include=${PROJECT_SOURCE_DIR}/include --source-dir ${CMAKE_CURRENT_SOURCE_DIR}
        WORKING_DIRECTORY ${PROJECT_SOURCE_DIR})

add_test(NAME unit_test COMMAND ${Python_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/unit_runner.py
        $<TARGET_FILE:unit_serial> --include=${PROJECT_SOURCE_DIR}/include --source-dir ${CMAKE_CURRENT_SOURCE_DIR}
        WORKING_DIRECTORY ${PROJECT_SOURCE_DIR})

add_test(NAME catch_test COMMAND ${Python_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/catch_runner.py
        $<TARGET_FILE:catch_serial> --include=${PROJECT_SOURCE_DIR}/include --source-dir ${CMAKE_CURRENT_SOURCE_DIR}
        WORKING_DIRECTORY ${PROJECT_SOURCE_DIR})

#set_target_properties(serial_compile_test_c   PROPERTIES COMPILE_FLAGS "-g -gdwarf-4 -Og -fno-omit-frame-pointer")
#set_target_properties(serial_compile_test_cpp PROPERTIES COMPILE_FLAGS "-g -gdwarf-4 -Og -fno-omit-frame-pointer")
set_tests_properties(read_test write_test newlib_blocked_test newlib_unchecked_test newlib_full_test argv_test unit_test catch_test PROPERTIES ENVIRONMENT PYTHONPATH=$PYTHONPATH:${PROJECT_SOURCE_DIR})