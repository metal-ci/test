/**
 * @file   argv.c
 * @date   17.06.2020
 * @author Klemens D. Morgenstern
 *
 */


#include <stdio.h>
#include <metal/serial/core.h>
#include <metal/serial/argv.h>


char metal_serial_read() { return (char)fgetc(stdin);}
void metal_serial_write(char c) { fputc(c, stdout);}

int main(int argc, char ** args)
{
    freopen(NULL, "rb", stdin);
    freopen(NULL, "wb", stdout);

    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);

    METAL_SERIAL_INIT();

    char buf[(sizeof(char*) * 2) + 16];

    metal_serial_init_argv(&argc, &args, buf, sizeof(buf));
    fprintf(stderr, "Argc: %d\n", argc);
    int i;
    for (i = 0; i < argc; i++)
        fprintf(stderr, "Writing argument %d: %s\n", i, args[i]);


#define METAL_SERIAL_TEST() METAL_SERIAL_WRITE_LOCATION()
    METAL_SERIAL_TEST();

    METAL_SERIAL_WRITE_INT(argc);
    for (i = 0; i < argc; i++)
        METAL_SERIAL_WRITE_STR(args[i]);


    METAL_SERIAL_EXIT(0);

    return 0;
}