/**
* @file   syscalls.c
* @date   03.07.2020
* @author Klemens D. Morgenstern
*
*/

#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>

#include <metal/break/core.h>
#include <errno.h>

int _open (char* file, int flags, int mode);
int _read (int file, char* ptr, int len);
int _write(int file, char* ptr, int len);
int _lseek(int file, int ptr, int dir);
int _close(int);


int _fstat(int fildes, struct stat* st)
{
    int res = -1;
    int err = 0;
    metal_break("syscalls.fstat", fildes, st, &res, &err);
    if (err)
        errno = err;
    return res;
}


int _stat(const char* file, struct stat* st)
{
    int res = -1;
    int err = 0;
    metal_break("syscalls.stat", file, st, &res, &err);
    if (err)
        errno = err;
    return res;
}

int _isatty(int file)
{
    int res = -1;
    int err = 0;
    metal_break("syscalls.isatty", file, &res, &err);
    if (err)
        errno = err;
    return res;
}


int _link(char* existing, char* _new)
{
    int res = -1;
    int err = 0;
    metal_break("syscalls.link", existing, _new, &res, &err);
    if (err)
        errno = err;
    return res;
}



int _symlink(const char* path1, const char* path2)
{
    int res = -1;
    int err = 0;
    metal_break("syscalls.symlink", path1, path2, &res, &err);
    if (err)
        errno = err;
    return res;
}

int _unlink(char* name)
{
    int res = -1;
    int err = 0;
    metal_break("syscalls.unlink", name, &res, &err);
    if (err)
        errno = err;
    return res;
}



int _open(char* file, int flags, int mode)
{
    int res = -1;
    int err = 0;
    metal_break("syscalls.open", file, flags, mode, &res, &err);
    if (err)
        errno = err;
    return res;
}




int _lseek(int file, int ptr, int dir)
{
    int res = -1;
    int err = 0;
    metal_break("syscalls.lseek", file, ptr, dir, &res, &err);
    if (err)
        errno = err;
    return res;
}




#if !defined(METAL_NEWLIB_BUFFER_SIZE) && !defined(METAL_NEWLIB_DISABLE_BUFFER)
#define METAL_NEWLIB_BUFFER_SIZE 0x400
#endif

#if defined(METAL_NEWLIB_BUFFER_SIZE)


//write buffer
static int write_fd  = -1;
static int write_pos = 0;
static char write_buf[METAL_NEWLIB_BUFFER_SIZE];

static void flush_write()
{
    if (write_pos > 0)
    {
        _write(write_fd, write_buf, write_pos);
        write_fd = -1;
        write_pos = 0;
    }
}

static int _buffered_write(int file, char* ptr, int len __attribute__((unused)))
{
    if ((file != write_fd) || (write_pos == METAL_NEWLIB_BUFFER_SIZE))
    {
        flush_write();
        write_fd = file;
    }

    write_buf[write_pos++] = *ptr;

    if (*ptr == '\n') //flush on newline, but put it into the buffer first.
    {
        flush_write();
        write_fd = file;
    }

    return 1;
}

int _write(int file, char* ptr, int len)
{
    if (len == 1)
        return _buffered_write(file, ptr, len);
    else
    {
        int res = -1;
        int err = 0;
        metal_break("syscalls.write", file, ptr, len, &res, &err);
        if (err)
            errno = err;
        return res;
    }
}


//read buffer
static int read_fd = -1;
static int read_pos = 0;
static int read_end = 0;
static char read_buf[METAL_NEWLIB_BUFFER_SIZE];

void read_clear()
{
    read_pos = 0;
    read_end = 0;
    read_fd = -1;
}

void _read_init_buffer(int fd)
{
    read_fd = fd;
    read_pos = 0;

    int buf_size = METAL_NEWLIB_BUFFER_SIZE;
    metal_break("syscalls.read_init_buffer", read_fd, buf_size, read_buf, &read_end);
}

int _read_buffered(char* ptr, int len)
{
    if( (read_pos == read_end) && (read_end == METAL_NEWLIB_BUFFER_SIZE))
    {
        read_pos = 0;

        int buf_size = METAL_NEWLIB_BUFFER_SIZE;
        metal_break("syscalls.read_buffered", read_fd, buf_size, read_buf, &read_end);
    }

    //read what's available
    int i = 0;
    for (; ((read_pos + i) < read_end) && (i<len); i++) //read current buffer
        ptr[i] = read_buf[read_pos+i];

    read_pos += i;
    return i;
}

int _read(int file, char* ptr, int len)
{
    if ((read_fd != -1) && (file == read_fd))
        return _read_buffered(ptr, len);
    else if ((read_fd == -1) && (len>0))
    {
        _read_init_buffer(file);
        return  _read_buffered(ptr, len);
    }
    else
    {
        int res = -1;
        int err = 0;
        metal_break("syscalls.read", file, ptr, len, &res, &err);
        if (err)
            errno = err;
        return res;
    }
}

int _close(int fildes)
{
    flush_write();
    if (read_fd == fildes)
        read_clear();


    int res = -1;
    int err = 0;
    metal_break("syscalls.close", fildes, &res, &err);
    if (err)
        errno = err;
    return res;
}

#else

int _write(int file, char* ptr, int len)
{
    int res = -1;
    int err = 0;
    metal_break("syscalls.write", file, ptr, len, &res, &err);
    if (err)
        errno = err;
    return res;
}

int _read(int file, char* ptr, int len)
{
    int res = -1;
    int err = 0;
    metal_break("syscalls.read", file, ptr, len, &res, &err);
    if (err)
        errno = err;
    return res;
}


int _close(int fildes)
{
    int res = -1;
    int err = 0;
    metal_break("syscalls.close", filedes, &res, &err);
    if (err)
        errno = err;
    return res;
}

#endif






