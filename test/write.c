/**
 * @file   write.c
 * @date   19.06.2020
 * @author Klemens D. Morgenstern
 *
 */

// !!! This test is line sensitive, do NOT change lines around.

#include <metal/serial.h>
#include <stdio.h>


char metal_serial_read() { return fgetc(stdin);}
void metal_serial_write(char c) { fputc(c, stdout);}

int main(int argc, char ** args)
{
    freopen(NULL, "rb", stdin);
    freopen(NULL, "wb", stdout);

    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);

    METAL_SERIAL_INIT();
    fprintf(stderr, "Target initialized\n");
    char c = 0;

    METAL_SERIAL_READ_BYTE(c);
    fprintf(stderr, "Target read byte %c\n", c);

    METAL_SERIAL_WRITE_BYTE(c + 9);
    fprintf(stderr, "Target wrote byte %c\n", c + 9);

    int i = 0;
    METAL_SERIAL_READ_INT(i);
    fprintf(stderr, "Target read int %d\n", i);
    METAL_SERIAL_WRITE_INT(i * 2);
    fprintf(stderr, "Target wrote int %d\n", i * 2);

    char buffer[7];
    METAL_SERIAL_READ_STR(buffer, 7);
    fprintf(stderr, "Target read str '%s'\n", buffer);

    METAL_SERIAL_WRITE_STR(buffer + 1);
    fprintf(stderr, "Target wrote str '%s'\n", buffer);


    METAL_SERIAL_READ_INT(i);
    fprintf(stderr, "Target read int %d\n", i);
    METAL_SERIAL_WRITE_INT(i * 3);
    fprintf(stderr, "Target wrote int %d\n", i * 3);

    METAL_SERIAL_READ_STR(buffer, 7);
    fprintf(stderr, "Target read str '%s'\n", buffer);

    METAL_SERIAL_WRITE_STR(buffer + 2);
    fprintf(stderr, "Target wrote str '%s'\n", buffer + 2);

    METAL_SERIAL_READ_INT(i);
    fprintf(stderr, "Target read int %d\n", i);
    METAL_SERIAL_WRITE_INT(i * 4);
    fprintf(stderr, "Target wrote int %d\n", i * 4);


    char memory[4];
    METAL_SERIAL_READ_MEMORY(memory, 4);
    char return_memory[4] = {memory[3], memory[2], memory[1], memory[0]};

    METAL_SERIAL_WRITE_MEMORY(return_memory, sizeof(return_memory));


    METAL_SERIAL_READ_MEMORY(memory, 4);
    METAL_SERIAL_WRITE_MEMORY(memory, 4);

    METAL_SERIAL_EXIT(123);
    return 0;
}