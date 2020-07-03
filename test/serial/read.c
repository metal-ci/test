/**
 * @file   read.c
 * @date   17.06.2020
 * @author Klemens D. Morgenstern
 *
 */

// !!! This test is line sensitive, do NOT change lines around.

#include <metal/serial/core.h>
#include <stdio.h>


char metal_serial_read() { return (char)fgetc(stdin);}
void metal_serial_write(char c) { fputc(c, stdout);}

int main(int argc, char ** args)
{
    freopen(NULL, "rb", stdin);
    freopen(NULL, "wb", stdout);

    METAL_SERIAL_INIT();
    int i = 42;

    METAL_SERIAL_WRITE_BYTE('a');
    METAL_SERIAL_WRITE_INT(42);
    METAL_SERIAL_WRITE_STR("test-string");
    METAL_SERIAL_WRITE_PTR(&main);
    METAL_SERIAL_WRITE_MEMORY(&i, sizeof(i));
    METAL_SERIAL_WRITE_INT(1234);

    METAL_SERIAL_EXIT(42);

    return 0;
}