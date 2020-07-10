/**
 * @file   syscalls.c
 * @date   03.07.2020
 * @author Klemens D. Morgenstern
 *
 */

#include <sys/types.h>
#include <sys/stat.h>
#include <metal/serial/core.h>
#include <metal/serial/syscalls.h>
#include <errno.h>
#include <unistd.h>

#define METAL_SERIAL_SYSCALL(...) METAL_SERIAL_WRITE_MARKER();


#if !defined(METAL_SERIAL_SYSCALLS_MODE) && !__PCPP_ALWAYS_TRUE__
#warning "'METAL_SERIAL_SYSCALLS_MODE' not defined, defaulting to METAL_SERIAL_SYSCALLS_MODE_UNCHECKED"
#define METAL_SERIAL_SYSCALLS_MODE METAL_SERIAL_SYSCALLS_MODE_UNCHECKED
#endif

#pragma GCC optimize "-O0"


int _open (char* file, int flags, int mode);
int _read (int file, char* ptr, int len);
int _write(int file, char* ptr, int len);
int _lseek(int file, int ptr, int dir);
int _close(int);


void _read_time_spec(struct timespec * ts)
{
    METAL_SERIAL_READ_INT(ts->tv_sec);
    METAL_SERIAL_READ_INT(ts->tv_nsec);
}

void _read_stat_impl(struct stat * st)
{
    METAL_SERIAL_READ_INT(st->st_dev);         /* ID of device containing file */
    METAL_SERIAL_READ_INT(st->st_ino);         /* Inode number */
    METAL_SERIAL_READ_INT(st->st_mode);        /* File type and mode */
    METAL_SERIAL_READ_INT(st->st_nlink);       /* Number of hard links */
    METAL_SERIAL_READ_INT(st->st_uid);         /* User ID of owner */
    METAL_SERIAL_READ_INT(st->st_gid);         /* Group ID of owner */
    METAL_SERIAL_READ_INT(st->st_rdev);        /* Device ID (if special file) */
    METAL_SERIAL_READ_INT(st->st_size);        /* Total size, in bytes */
    METAL_SERIAL_READ_INT(st->st_blksize);     /* Block size for filesystem I/O */
    METAL_SERIAL_READ_INT(st->st_blocks);      /* Number of 512B blocks allocated */

    /* Since Linux 2.6, the kernel supports nanosecond
       precision for the following timestamp fields.
       For the details before Linux 2.6, see NOTES. */

    _read_time_spec(&st->st_atim);  /* Time of last access */
    _read_time_spec(&st->st_mtim);  /* Time of last modification */
    _read_time_spec(&st->st_ctim);  /* Time of last status change */
}

int _fstat(int fildes, struct stat* st)
{
#if METAL_SERIAL_SYSCALLS_MODE == METAL_SERIAL_SYSCALLS_MODE_FULL
    METAL_SERIAL_SYSCALL(fstat);
    METAL_SERIAL_WRITE_INT(fildes);
    int res = 0;
    METAL_SERIAL_READ_INT(res);
    if (res != 0)
    {
        errno = res;
        return -1;
    }
    else
        _read_stat_impl(st);
    return 0;
#else
    errno = EIO;
    return -1;
#endif
}



int _stat(const char* file, struct stat* st)
{
#if METAL_SERIAL_SYSCALLS_MODE == METAL_SERIAL_SYSCALLS_MODE_FULL
    METAL_SERIAL_SYSCALL(stat);
    METAL_SERIAL_WRITE_STR(file);
    int err = 0;
    METAL_SERIAL_READ_INT(err);
    if (err != 0)
    {
        errno = err;
        return -1;
    }
    else
        _read_stat_impl(st);
    return 0;
#else
    errno = EIO;
    return -1;
#endif
}

int _isatty(int file)
{
#if METAL_SERIAL_SYSCALLS_MODE == METAL_SERIAL_SYSCALLS_MODE_FULL
    METAL_SERIAL_SYSCALL(isatty);
    METAL_SERIAL_WRITE_INT(file);

    int err = 0;
    METAL_SERIAL_READ_INT(err);
    if (err != 0)
    {
        errno = err;
        return -1;
    }

    int res = 0;
    METAL_SERIAL_READ_INT(res);
    return res;
#elif METAL_SERIAL_SYSCALLS_MODE == METAL_SERIAL_SYSCALLS_MODE_BLOCKED
    errno = EBADF;
    return -1;
#else
    return 0;
#endif
}


int _link(char* existing, char* _new)
{
#if METAL_SERIAL_SYSCALLS_MODE == METAL_SERIAL_SYSCALLS_MODE_FULL
    METAL_SERIAL_SYSCALL(link);

    METAL_SERIAL_WRITE_STR(existing);
    METAL_SERIAL_WRITE_STR(_new);

    int err = 0;
    METAL_SERIAL_READ_INT(err);
    if (err != 0)
    {
        errno = err;
        return -1;
    }
    return 0;
#else
    errno = EACCES;
    return -1;
#endif
}


int _symlink(const char* path1, const char* path2)
{
#if METAL_SERIAL_SYSCALLS_MODE == METAL_SERIAL_SYSCALLS_MODE_FULL
    METAL_SERIAL_SYSCALL(symlink);

    METAL_SERIAL_WRITE_STR(path1);
    METAL_SERIAL_WRITE_STR(path2);

    int err = 0;
    METAL_SERIAL_READ_INT(err);
    if (err != 0)
    {
        errno = err;
        return -1;
    }
    return 0;
#else
    errno = EACCES;
    return -1;
#endif
}




int _unlink(char* name)
{
#if METAL_SERIAL_SYSCALLS_MODE == METAL_SERIAL_SYSCALLS_MODE_FULL
    METAL_SERIAL_SYSCALL(unlink);
    METAL_SERIAL_WRITE_STR(name);
    int err = 0;
    METAL_SERIAL_READ_INT(err);
    if (err != 0)
    {
        errno = err;
        return -1;
    }
    return 0;
#else
    errno = EACCES;
    return -1;
#endif
}



int _lseek(int file, int ptr, int dir)
{
#if METAL_SERIAL_SYSCALLS_MODE == METAL_SERIAL_SYSCALLS_MODE_FULL
    METAL_SERIAL_SYSCALL(unlink);

    METAL_SERIAL_WRITE_INT(file);
    METAL_SERIAL_WRITE_INT(ptr);
    METAL_SERIAL_WRITE_INT(dir);

    int res = 0;
    METAL_SERIAL_READ_INT(res);
    if (res == -1)
    {
        int err = 0;
        METAL_SERIAL_READ_INT(err);
        errno = err;
        return -1;
    }
    return res;
#else
    errno = EACCES;
    return -1;
#endif
}

#if METAL_SERIAL_SYSCALLS_MODE == METAL_SERIAL_SYSCALLS_MODE_UNCHECKED
static int _open_fd_gen = 2;
#endif


int _open(char* file, int flags, int mode)
{
#if METAL_SERIAL_SYSCALLS_MODE == METAL_SERIAL_SYSCALLS_MODE_FULL
    METAL_SERIAL_SYSCALL(open, full);
    METAL_SERIAL_WRITE_STR(file);
    METAL_SERIAL_WRITE_INT(flags);
    METAL_SERIAL_WRITE_INT(mode);
    int res = 0;
    METAL_SERIAL_READ_INT(res);
    if (res == -1)
    {
        int err = 0;
        METAL_SERIAL_READ_INT(err);
        errno = err;
        return -1;
    }
    return res;
#elif METAL_SERIAL_SYSCALLS_MODE == METAL_SERIAL_SYSCALLS_MODE_UNCHECKED
    METAL_SERIAL_SYSCALL(open, unchecked);
    //can only write!
    if ((flags & O_RDWR) || (flags & O_RDONLY))
    {
        errno = EACCES;
        return -1;
    }

    METAL_SERIAL_WRITE_STR(file);
    METAL_SERIAL_WRITE_INT(flags);
    METAL_SERIAL_WRITE_INT(mode);
    int fd = ++_open_fd_gen;

    METAL_SERIAL_WRITE_INT(fd);
    return fd;
#else
    errno = EACCES;
    return -1;
#endif
}


int _close(int fildes)
{
#if METAL_SERIAL_SYSCALLS_MODE == METAL_SERIAL_SYSCALLS_MODE_FULL
    METAL_SERIAL_SYSCALL(close, full);
    METAL_SERIAL_WRITE_INT(fildes);

    int err = 0;
    METAL_SERIAL_READ_INT(err);
    if (err != 0)
    {
        errno = err;
        return -1;
    }
    return 0;

#elif METAL_SERIAL_SYSCALLS_MODE == METAL_SERIAL_SYSCALLS_MODE_UNCHECKED
    METAL_SERIAL_SYSCALL(close, unchecked);
    METAL_SERIAL_WRITE_INT(fildes);
    return 0;
#else
    errno = EBADF;
    return -1;
#endif
}

#if METAL_SERIAL_SYSCALLS_MODE == METAL_SERIAL_SYSCALLS_MODE_BLOCKED

int _write(int file, char* ptr, int len)
{
    if ((file == STDOUT_FILENO) || (file == STDERR_FILENO))
    {
        METAL_SERIAL_SYSCALL(write, blocked);
        METAL_SERIAL_WRITE_INT(file);
        METAL_SERIAL_WRITE_MEMORY(ptr, len);
        return len;
    }
    errno = EBADF;
    return -1;
}


int _read(int file, char* ptr, int len)
{
    errno = EBADF;
    return -1;
}
#else


int _write_impl(int file, char* ptr, int len)
{
#if METAL_SERIAL_SYSCALLS_MODE == METAL_SERIAL_SYSCALLS_MODE_FULL
    METAL_SERIAL_SYSCALL(write, full);
    METAL_SERIAL_WRITE_INT(file);
    METAL_SERIAL_WRITE_MEMORY(ptr, len);

    int res = 0;
    METAL_SERIAL_READ_INT(res);
    if (res == -1)
    {
        int err;
        METAL_SERIAL_READ_INT(err);
        errno = err;
        return -1;
    }
    return res;
#else
    METAL_SERIAL_SYSCALL(write, unchecked);
    METAL_SERIAL_WRITE_INT(file);
    METAL_SERIAL_WRITE_MEMORY(ptr, len);
    return len;
#endif
}

int _read_impl(int file, char* ptr, int len)
{
#if METAL_SERIAL_SYSCALLS_MODE == METAL_SERIAL_SYSCALLS_MODE_FULL
    METAL_SERIAL_SYSCALL(read, full);
    METAL_SERIAL_WRITE_INT(file);
    METAL_SERIAL_WRITE_INT(len);
    int err;
    METAL_SERIAL_READ_INT(err);
    if (err != 0)
    {
        errno = err;
        return -1;
    }
    int read_len = 0;
    METAL_SERIAL_READ_MEMORY(ptr, len, read_len);
    return read_len;
#else
    errno = EBADF;
    return -1;
#endif
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
        _write_impl(write_fd, write_buf, write_pos);
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

    if ((*ptr == '\n')) //flush on newline, but put it into the buffer first.
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
        return _write_impl(file, ptr, len);
}


#if METAL_SERIAL_SYSCALLS_MODE == METAL_SERIAL_SYSCALLS_MODE_FULL

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


int _read_buffered_impl(int file, char* ptr, int len)
{
    METAL_SERIAL_SYSCALL(read, buffered);
    METAL_SERIAL_WRITE_INT(file);
    METAL_SERIAL_WRITE_INT(len);

    int err;
    METAL_SERIAL_READ_INT(err);

    if (err != 0)
    {
        errno = err;
        return -1;
    }

    int read_len = 0;
    METAL_SERIAL_READ_MEMORY(ptr, len, read_len);

    return read_len;
}


void _read_init_buffer(int fd)
{
    read_fd = fd;
    read_pos = 0;

    read_end = _read_buffered_impl(read_fd, read_buf, METAL_NEWLIB_BUFFER_SIZE);

}

int _read_buffered(char* ptr, int len)
{
    if( (read_pos == read_end) && (read_end == METAL_NEWLIB_BUFFER_SIZE))
    {
        read_pos = 0;
        read_end = _read_buffered_impl(read_fd, read_buf, METAL_NEWLIB_BUFFER_SIZE);
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
        return _read_impl(file, ptr, len);
}

#else
int _read (int file, char* ptr, int len) __attribute__((alias( "_read_impl")));
#endif

#else //unbuffered

int _read (int file, char* ptr, int len) __attribute__((alias( "_read_impl")));
int _write(int file, char* ptr, int len) __attribute__((alias("_write_impl")));

#endif

#endif