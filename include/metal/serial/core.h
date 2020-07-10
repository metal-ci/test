#ifndef METAL_SERIAL_H_
#define METAL_SERIAL_H_

#if defined(__cplusplus)
#include <cstdint>
extern "C" {
#else

#include <stdint.h>

#endif

void metal_serial_write(char);
char metal_serial_read();

#if defined(__cplusplus)
}
#endif

#define METAL_SERIAL_VERSION_STRING "__metal_serial_version_1"

#define METAL_SERIAL_WRITE_BYTE(value) \
    metal_serial_write(value);

#define METAL_SERIAL_READ_BYTE(value) \
    {value = metal_serial_read();}

#define METAL_SERIAL_WRITE_INT(value)                       \
{                                                           \
    metal_serial_write(sizeof(value));                      \
    unsigned int idx;                                       \
    for (idx = 0u; idx < sizeof(value); idx++)              \
         metal_serial_write((value) >> (idx << 3u));        \
}


#define METAL_SERIAL_READ_INT(value)                        \
{                                                           \
    const char sz = metal_serial_read();                    \
    (value) = 0;                                            \
    unsigned int idx;                                       \
    for (idx = 0u; idx < sz; idx++)                         \
         (value) |= (metal_serial_read() & 0xFF) << (idx << 3u);     \
}


#define METAL_SERIAL_WRITE_STR(value)                  \
    {                                                  \
        unsigned int strlen = 0;                       \
        while((value)[strlen++] != '\0');              \
        unsigned int idx;                              \
        for (idx = 0u; idx<strlen; idx++)              \
            metal_serial_write((value)[idx]);          \
    }                                                  \


#define METAL_SERIAL_READ_STR(value, buffer_size)       \
    {                                                   \
        unsigned int idx_ = 0u;                         \
        int null_terminated = 0;                        \
        for (; idx_<(buffer_size - 1); idx_++)          \
        {                                               \
            const char next = metal_serial_read();      \
            (value)[idx_] = next;                       \
            if (next == '\0')                           \
            {                                           \
                null_terminated = 1;                    \
                break;                                  \
            }                                           \
        }                                               \
        if (!null_terminated)                           \
        {                                               \
            (value)[buffer_size-1] = '\0';              \
            while (metal_serial_read() != '\0');        \
        }                                               \
        METAL_SERIAL_WRITE_INT(idx_);                   \
    }                                                   \


#define METAL_SERIAL_WRITE_MEMORY(pointer, size)    \
    METAL_SERIAL_WRITE_INT(size);                   \
    {                                               \
        unsigned int idx;                           \
        for (idx = 0u; idx < size; idx++)           \
        metal_serial_write(((char*)(pointer))[idx]); }

#define METAL_SERIAL_READ_MEMORY(pointer, buffer_size, read_size)  \
    { \
        unsigned int size = 0u;                             \
        METAL_SERIAL_READ_INT(size);                        \
        read_size = size;                                   \
        unsigned int idx;                                   \
        if (read_size > buffer_size)                        \
            read_size = buffer_size;                        \
        for (idx = 0u; idx < read_size; idx++)              \
            ((char*)(pointer))[idx] = metal_serial_read();  \
        for (idx = read_size; idx < size; idx++)            \
            (void)metal_serial_read();                      \
        METAL_SERIAL_WRITE_INT(read_size);                  \
    }


#if defined(__cplusplus)
#define METAL_SERIAL_WRITE_PTR(value) METAL_SERIAL_WRITE_INT((std::uintptr_t)value)
#else
#define METAL_SERIAL_WRITE_PTR(value) METAL_SERIAL_WRITE_INT((uintptr_t)value)
#endif

#define METAL_SERIAL_WRITE_LOCATION_IMPL(CNT) \
    { \
        __asm("__metal_serial_" #CNT ":" ); \
        extern const int __location_ ##CNT __asm("__metal_serial_" #CNT);   \
        METAL_SERIAL_WRITE_PTR(&__location_ ##CNT);  \
    }

#define METAL_SERIAL_WRITE_LOCATION_IMPL2(CNT) METAL_SERIAL_WRITE_LOCATION_IMPL(CNT)

#define METAL_SERIAL_WRITE_LOCATION() METAL_SERIAL_WRITE_LOCATION_IMPL2(__COUNTER__)

#define METAL_SERIAL_WRITE_MARKER(...) METAL_SERIAL_WRITE_LOCATION()

#define METAL_SERIAL_INIT()                                                         \
  {                                                                                 \
    unsigned int idx;                                                               \
    for (idx = 0u; idx < sizeof(METAL_SERIAL_VERSION_STRING); idx++)                \
        metal_serial_write(METAL_SERIAL_VERSION_STRING[idx]);                       \
    int metal_serial_init = 0x6C43;                                                 \
    metal_serial_write(sizeof(metal_serial_init));                                  \
    char* p = (char*)&metal_serial_init;                                            \
    for (idx = 0u; idx < sizeof(metal_serial_init); idx++)                          \
        metal_serial_write(p[idx]);                                                 \
    METAL_SERIAL_WRITE_PTR(&metal_serial_write);                                    \
    METAL_SERIAL_WRITE_LOCATION();                                                  \
  }

#define METAL_SERIAL_EXIT(Value) METAL_SERIAL_WRITE_MARKER(metal.exit); METAL_SERIAL_WRITE_INT(Value);

#endif //METAL_SERIAL_MACROS_H