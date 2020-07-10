/**
 * @file   newlib_blocked.c
 * @date   17.06.2020
 * @author Klemens D. Morgenstern
 *
 */

// !!! This test is line sensitive, do NOT change lines around.

#include <metal/serial/core.h>
#include <metal/serial/syscalls.h>
#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
#include <errno.h>

int _open (char* file, int flags, int mode);
int _read (int file, char* ptr, int len);
int _write(int file, char* ptr, int len);
int _lseek(int file, int ptr, int dir);
int _close(int);


char metal_serial_read() { return fgetc(stdin);}
void metal_serial_write(char c) { fputc(c, stdout);}

int main(int argc, char ** args)
{
    freopen(NULL, "rb", stdin);
    freopen(NULL, "wb", stdout);

    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);

    METAL_SERIAL_INIT();

    int len = sizeof("Writing stdout\n") - 1;
    int res = 0;
    if ((_write(STDOUT_FILENO, "Writing stdout\n", len) != len) || errno)
        res ++;
    if ((_write(STDERR_FILENO, "Writing stderr\n", len) !=len) || errno)
        res ++;

    int fd = _open(__FILE__, O_RDONLY, 0);
    if ((fd != -1) || errno != EACCES)
        res ++;

    errno = 0;
    int cres = _close(STDOUT_FILENO);
    if ((cres != -1) || errno != EBADF)
        res ++;

    METAL_SERIAL_EXIT(res);

    return res;
}