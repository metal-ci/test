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
#include <assert.h>

int _open (char* file, int flags, int mode);
int _read (int file, char* ptr, int len);
int _write(int file, char* ptr, int len);
int _lseek(int file, int ptr, int dir);
int _close(int);
int _isatty(int file);
int _stat(const char* file, struct stat* st);
int _fstat(int fd, struct stat* st);

int _link(char* existing, char* _new);
int _symlink(char* existing, char* _new);
int _unlink(char* existing);

char metal_serial_read() { return fgetc(stdin);}
void metal_serial_write(char c) { fputc(c, stdout);}


int main(int argc, char ** args)
{
    freopen(NULL, "rb", stdin);
    freopen(NULL, "wb", stdout);

    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);

    METAL_SERIAL_INIT();

    int res = 0;

    struct stat st;
    assert(_stat(__FILE__, &st) != 0);
    assert(errno == 2);

    errno = 0;

    int len = sizeof("Writing stdout\n") - 1;
    assert(_write(STDOUT_FILENO, "Writing stdout\n", len) == len);
    assert(errno == 0);

    assert(_write(STDERR_FILENO, "Writing stderr\n", len) ==len);
    assert(errno == 0);

    errno = 0;
    assert(_isatty(STDOUT_FILENO) == 0);
    assert(errno == 0);

    assert(_isatty(STDERR_FILENO) != 0);
    assert(errno == 0);

    char buf[10];
    assert(_read(STDIN_FILENO, buf, 5) == 5);
    assert(errno == 0);
    assert(buf[0] == 's');
    assert(buf[1] == 't');
    assert(buf[2] == 'd');
    assert(buf[3] == 'i');
    assert(buf[4] == 'n');


    int fd = _open("test-file", O_RDWR, 0);
    assert(fd == 3);
    assert(errno == 0);

    assert(_write(fd, "Writing to fd_\n", len) == len);
    assert(errno == 0);


    assert(_read(fd, buf, 5) == 5);
    assert(errno == 0);
    assert(buf[0] == 't');
    assert(buf[1] == 'e');
    assert(buf[2] == 's');
    assert(buf[3] == 't');
    assert(buf[4] == 'f');


    assert(_fstat(fd, &st) == 0);
    assert(errno == 0);

    assert(st.st_dev == 1);
    assert(st.st_ino == 2);
    assert(st.st_nlink == 4);
    assert(st.st_uid == 5);
    assert(st.st_gid == 6);

    assert(st.st_size == 1024);
    assert(st.st_atim.tv_sec  == 900);
    assert(st.st_atim.tv_nsec == 800);
    assert(st.st_mtim.tv_sec  == 3000);
    assert(st.st_ctim.tv_sec  == 5000);

    errno = 0;
    assert(_close(fd) == 0);
    assert(errno == 0);

    assert(_link("syscalls.h", "lib/syscalls.c") == 0);
    assert(errno == 0);

    assert(_unlink("syscalls.h") == 0);
    assert(errno == 0);

    assert(_symlink("doesn't exist", "lib/syscalls.h") != 0);
    assert(errno == ENOENT);

    METAL_SERIAL_EXIT(res);

    return res;
}