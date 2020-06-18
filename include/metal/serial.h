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
    metal_serial_write(1, &value);

#define METAL_SERIAL_WRITE_INT(value)                       \
    metal_serial_write(sizeof(value));                      \
    for (unsigned int idx = 0u; idx < sizeof(value); idx++) \
         metal_serial_write(value >> (idx << 3u));          \


#define METAL_SERIAL_READ_INT(value)                        \
{                                                           \
    char sz = metal_serial_write();                          \
    value = 0;                                              \
    for (unsigned int idx = 0u; idx < sizeof(value); idx++) \
         value |= metal_serial_write(value) << (idx << 3);  \
}


#define METAL_SERIAL_WRITE_STR(value)                  \
    {                                                  \
        unsigned int strlen = 0;                       \
        while(value[strlen++] != '\0');                \
        for (unsigned int idx = 0u; idx<strlen; idx++) \
            metal_serial_write(value[idx]);            \
    }                                                  \


#define METAL_SERIAL_READ_STR(value, buffer_size)      \
    {                                                  \
        unsigned int strlen = 0u;                      \
        METAL_READ_INT(strlen);                       \
        if (strlen >= buffer_size)                     \
            strlen = buffer_size;                      \
        for (unsigned int idx = 0u; idx<strlen; idx++) \
            metal_serial_write(idx[value]);            \
        value[buffer_size - 1] = '\0';                 \
        METAL_SERIAL_WRITE_INT(strlen);               \
    }                                                  \


#define METAL_SERIAL_WRITE_MEMORY(pointer, size)    \
    METAL_SERIAL_WRITE_INT(size);                  \
    for (unsigned int idx = 0u; idx < size; idx++)  \
        metal_serial_write(((char*)pointer)[idx]);

#define METAL_SERIAL_READ_MEMORY(pointer, buffer_size)  \
    { \
        unsigned int size = 0u;                             \
        METAL_SERIAL_READ_INT(size);                       \
        if (size > buffer_size)                             \
            size = buffer_size;                             \
        for (unsigned int idx = 0u; idx < size; idx++)      \
            metal_serial_write(idx[(char*)pointer]);        \
        METAL_SERIAL_WRITE_INT(size);                      \
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


#if !defined(METAL_OVERLOAD)
#define METAL_CONCAT_IMPL(x, y) x##y
#define METAL_CONCAT(x, y) METAL_CONCAT_IMPL( x, y )

#define METAL_STRINGIZE(x) METAL_STRINGIZE2(x)
#define METAL_STRINGIZE2(x) #x
#define METAL_LOCATION_STR() __FILE__ "(" METAL_STRINGIZE(__LINE__) ")"

#define METAL_PP_NARG(...)  METAL_PP_NARG_(__VA_ARGS__,METAL_PP_RSEQ_N())
#define METAL_PP_NARG_(...) METAL_PP_ARG_N(__VA_ARGS__)
#define METAL_PP_ARG_N(_1, _2, _3, _4, _5, _6, _7, _8, _9, _A, _B, _C, _D, _E, _F, N, ...) N
#define METAL_PP_RSEQ_N() F, E, D, C, B, A, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0

#define METAL_OVERLOAD(Macro, ...) METAL_CONCAT(Macro, METAL_PP_NARG(__VA_ARGS__)) (__VA_ARGS__)
#endif


#define METAL_SERIAL_EXIT(Value) METAL_SERIAL_WRITE_LOCATION(); METAL_SERIAL_WRITE_INT(Value);



#endif