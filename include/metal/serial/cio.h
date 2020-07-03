#ifndef METAL_SERIAL_CIO_H
#define METAL_SERIAL_CIO_H

#include <metal/serial/core.h>
#include <metal/macros.h>

#define METAL_PRINTF_STEP(Invocation) METAL_SERIAL_WRITE_##Invocation

#define METAL_STDIN  0
#define METAL_STDOUT 1
#define METAL_STDERR 2

// METAL_PRINT_FORMAT(Format, Value)
// METAL_PRINT_FILE(Handle)
#define METAL_PRINT(Format, ...) METAL_SERIAL_WRITE_LOCATION(); METAL_PP_FOR_EACH(METAL_SERIAL_PRINT_STEP, __VA_ARGS__);
#define METAL_INPUT(Format, ...) METAL_SERIAL_WRITE_LOCATION(); METAL_PP_FOR_EACH(METAL_SERIAL_INPUT_STEP, __VA_ARGS__);

#define METAL_WRITE(FileHandle, Memory, Size) METAL_SERIAL_WRITE_LOCATION(); METAL_SERIAL_WRITE_MEMORY(Memory, Size);
#define METAL_READ (FileHandle, Memory, Size) METAL_SERIAL_WRITE_LOCATION(); METAL_SERIAL_READ_MEMORY(Memory, Size);

#define METAL_OPEN_2(Filename, Mode)
#define METAL_OPEN_1(Filename, Mode) METAL_OPEN_2(Filename, "r")
#define METAL_OPEN(...) METAL_PP_OVERLOAD(METAL_OPEN_, __VA_ARGS__) (__VA_ARGS__)

#endif //METAL_SERIAL_CIO_H
