#ifndef METAL_SERIAL_H_
#define METAL_SERIAL_H_

#if defined(__cplusplus)
extern "C" {
#include <cstdint>
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
    metal_serial_write(sizeof(value));                      \
    for (unsigned int idx = 0u; idx < sizeof(value); idx++) \
         metal_serial_write((value) >> (idx << 3u));        \


#define METAL_SERIAL_READ_INT(value)                        \
{                                                           \
    const char sz = metal_serial_read();                    \
    fprintf(stderr, "Target int sz %d\n", sz);              \
    (value) = 0;                                            \
    for (unsigned int idx = 0u; idx < sz; idx++)            \
         (value) |= metal_serial_read() << (idx << 3);      \
}


#define METAL_SERIAL_WRITE_STR(value)                  \
    {                                                  \
        unsigned int strlen = 0;                       \
        while((value)[strlen++] != '\0');              \
        for (unsigned int idx = 0u; idx<strlen; idx++) \
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
    for (unsigned int idx = 0u; idx < size; idx++)  \
        metal_serial_write(((char*)(pointer))[idx]);

#define METAL_SERIAL_READ_MEMORY(pointer, buffer_size)  \
    { \
        unsigned int size = 0u;                             \
        METAL_SERIAL_READ_INT(size);                        \
        unsigned int read_size = size;                      \
        if (read_size > buffer_size)                        \
            read_size = buffer_size;                        \
        for (unsigned int idx = 0u; idx < read_size; idx++) \
            ((char*)(pointer))[idx] = metal_serial_read();  \
        for (unsigned int idx = read_size; idx < size; idx++) \
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
        extern const int __metal_serial_ ## CNT;   \
        METAL_SERIAL_WRITE_PTR(&__metal_serial_ ## CNT);  \
    }

#define METAL_SERIAL_WRITE_LOCATION_IMPL2(CNT) METAL_SERIAL_WRITE_LOCATION_IMPL(CNT)

#define METAL_SERIAL_WRITE_LOCATION() METAL_SERIAL_WRITE_LOCATION_IMPL2(__COUNTER__)

#define METAL_SERIAL_INIT()                                                         \
  {  for (unsigned int idx = 0u; idx < sizeof(METAL_SERIAL_VERSION_STRING); idx++)  \
        metal_serial_write(METAL_SERIAL_VERSION_STRING[idx]);                       \
    int metal_serial_init = 0x6C43;                                                 \
    metal_serial_write(sizeof(metal_serial_init));                                  \
    char* p = (char*)&metal_serial_init;                                            \
    for (unsigned int idx = 0u; idx < sizeof(metal_serial_init); idx++)             \
        metal_serial_write(p[idx]);                                                 \
    METAL_SERIAL_WRITE_PTR(&metal_serial_write);                                    \
    METAL_SERIAL_WRITE_LOCATION(); }

#define METAL_SERIAL_EXIT(Value) METAL_SERIAL_WRITE_LOCATION(); METAL_SERIAL_WRITE_INT(Value);

#define METAL_SERIAL_WRITE_WITH_TYPE_BYTE(Value)         METAL_SERIAL_WRITE_BYTE('b') METAL_SERIAL_WRITE_BYTE(Value)
#define METAL_SERIAL_WRITE_WITH_TYPE_INT(Value)          METAL_SERIAL_WRITE_BYTE('i') METAL_SERIAL_WRITE_INT(Value)
#define METAL_SERIAL_WRITE_WITH_TYPE_STR(Value)          METAL_SERIAL_WRITE_BYTE('s') METAL_SERIAL_WRITE_STR(Value)
#define METAL_SERIAL_WRITE_WITH_TYPE_MEMORY(Value,Size)  METAL_SERIAL_WRITE_BYTE('x') METAL_SERIAL_WRITE_MEMORY(Value, Size)
#define METAL_SERIAL_WRITE_WITH_TYPE_PTR(Value)          METAL_SERIAL_WRITE_BYTE('p') METAL_SERIAL_WRITE_PTR(Value)
#define METAL_SERIAL_WRITE_WITH_TYPE_LOCATION()          METAL_SERIAL_WRITE_BYTE('l') METAL_SERIAL_WRITE_LOCATION()

#define METAL_SERIAL_READ_WITH_TYPE_BYTE(Value)    METAL_SERIAL_WRITE_BYTE('b') METAL_SERIAL_READ_BYTE(Value)
#define METAL_SERIAL_READ_WITH_TYPE_INT(Value)     METAL_SERIAL_WRITE_BYTE('i') METAL_SERIAL_READ_INT(Value)
#define METAL_SERIAL_READ_WITH_TYPE_STR(Value)     METAL_SERIAL_WRITE_BYTE('s') METAL_SERIAL_READ_STR(Value)
#define METAL_SERIAL_READ_WITH_TYPE_MEMORY(Value)  METAL_SERIAL_WRITE_BYTE('x') METAL_SERIAL_READ_MEMORY(Value)
#define METAL_SERIAL_READ_WITH_TYPE_LOCATION()     METAL_SERIAL_WRITE_BYTE('l') METAL_SERIAL_READ_LOCATION()

#endif //METAL_SERIAL_MACROS_H