/**
 * @file   argv_gdb.c
 * @date   14.07.2020
 * @author Klemens D. Morgenstern
 *
 */


#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
#include <errno.h>
#include <assert.h>
#include <metal/gdb/core.h>


int _main(int argc, char ** args)
{
    int res = 0;

    fprintf(stderr, "Argc: %d\n", argc);
    int i;
    for (i = 0; i < argc; i++)
        fprintf(stderr, "Writing argument %d: %s\n", i, args[i]);


    return res;
}

int main(int argc, char * argv[])
{
    metal_break("argv", argc, argv);

    int res = _main(argc, argv);
    _exit(res);
    return res;
}