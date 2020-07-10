import errno
import os
import stat


class Flags:
    # copied from https://github.com/bminor/newlib/blob/master/newlib/libc/include/sys/_default_fcntl.h

    _FOPEN      = (-1)          # # from sys/file.h, kernel use only
    _FREAD      = 0x0001        # read enabled
    _FWRITE     = 0x0002        # write enabled
    _FAPPEND    = 0x0008        # append (writes guaranteed at the end)
    _FMARK      = 0x0010        # internal; mark during gc()
    _FDEFER     = 0x0020        # internal; defer for next gc pass
    _FASYNC     = 0x0040        # signal pgrp when data ready
    _FSHLOCK    = 0x0080        # BSD flock() shared lock present
    _FEXLOCK    = 0x0100        # BSD flock() exclusive lock present
    _FCREAT     = 0x0200        # open with file create
    _FTRUNC     = 0x0400        # open with truncation
    _FEXCL      = 0x0800        # error on open if file exists
    _FNBIO      = 0x1000        # non blocking I/O (sys5 style)
    _FSYNC      = 0x2000        # do all writes synchronously
    _FNONBLOCK  = 0x4000        # non blocking I/O (POSIX style)
    _FNDELAY    = _FNONBLOCK    # non blocking I/O (4.2 style)
    _FNOCTTY    = 0x8000        # don't assign a ctty on this open

    _FBINARY    = 0x10000
    _FTEXT      = 0x20000
    _FNOINHERIT = 0x40000
    _FDIRECT    = 0x80000
    _FNOFOLLOW  = 0x100000
    _FDIRECTORY = 0x200000
    _FEXECSRCH  = 0x400000
    _FTMPFILE   = 0x800000
    _FNOATIME   = 0x1000000
    _FPATH      = 0x2000000

    O_RDONLY    = 0        # +1 == FREAD
    O_WRONLY    = 1        # +1 == FWRITE
    O_RDWR      = 2        # +1 == FREAD|FWRITE
    O_APPEND    = _FAPPEND
    O_CREAT     = _FCREAT
    O_TRUNC     = _FTRUNC
    O_EXCL      = _FEXCL
    O_SYNC      = _FSYNC
    O_NONBLOCK  = _FNONBLOCK
    O_NOCTTY    = _FNOCTTY
    O_CLOEXEC   = _FNOINHERIT
    O_NOFOLLOW  = _FNOFOLLOW
    O_DIRECTORY = _FDIRECTORY
    O_EXEC      = _FEXECSRCH
    O_SEARCH    = _FEXECSRCH

    O_DIRECT  = _FDIRECT

    O_BINARY  = _FBINARY
    O_TEXT    = _FTEXT
    O_DSYNC   = _FSYNC
    O_RSYNC   = _FSYNC

    O_TMPFILE = _FTMPFILE
    O_NOATIME = _FNOATIME
    O_PATH    = _FPATH
    O_ACCMODE   = (O_RDONLY|O_WRONLY|O_RDWR)

    O_NDELAY =_FNDELAY


    FAPPEND = _FAPPEND
    FSYNC   = _FSYNC
    FASYNC  = _FASYNC
    FNBIO   = _FNBIO
    FNONBIO = _FNONBLOCK    # XXX fix to be NONBLOCK everywhere
    FNDELAY = _FNDELAY

    FREAD    = _FREAD
    FWRITE   = _FWRITE
    FMARK    = _FMARK
    FDEFER   = _FDEFER
    FSHLOCK  = _FSHLOCK
    FEXLOCK  = _FEXLOCK
    FOPEN    = _FOPEN
    FCREAT   = _FCREAT
    FTRUNC   = _FTRUNC
    FEXCL    = _FEXCL
    FNOCTTY  = _FNOCTTY


    FNONBLOCK = _FNONBLOCK

    FD_CLOEXEC = 1    # posix

    F_DUPFD   = 0    # Duplicate fildes
    F_GETFD   = 1    # Get fildes flags (close on exec)
    F_SETFD   = 2    # Set fildes flags (close on exec)
    F_GETFL   = 3    # Get file flags
    F_SETFL   = 4    # Set file flags
    F_GETOWN  = 5    # Get owner - for ASYNC
    F_SETOWN  = 6    # Set owner - for ASYNC
    F_GETLK   = 7    # Get record-locking information
    F_SETLK   = 8    # Set or Clear a record-lock (Non-Blocking)
    F_SETLKW  = 9    # Set or Clear a record-lock (Blocking)
    F_RGETLK  = 10    # Test a remote lock to see if it is blocked
    F_RSETLK  = 11    # Set or unlock a remote lock
    F_CNVT    = 12    # Convert a fhandle to an open fd
    F_RSETLKW = 13    # Set or Clear remote record-lock(Blocking)


    F_DUPFD_CLOEXEC = 14    # As F_DUPFD, but set close-on-exec flag

    F_RDLCK = 1    # read lock
    F_WRLCK = 2    # write lock
    F_UNLCK = 3    # remove lock(s)

    F_UNLKSYS = 4    # remove remote locks for a given system

    AT_FDCWD =  -2
    AT_EACCESS          = 1
    AT_SYMLINK_NOFOLLOW = 2
    AT_SYMLINK_FOLLOW   = 4
    AT_REMOVEDIR        = 8

    AT_EMPTY_PATH       = 16

    LOCK_SH = 0x01        # shared file lock
    LOCK_EX = 0x02        # exclusive file lock
    LOCK_NB = 0x04        # don't block when locking
    LOCK_UN = 0x08        # unlock file

    # copied from https://github.com/bminor/newlib/blob/master/newlib/libc/include/sys/stat.h

    _IFMT   = 0o170000 # type of file
    _IFDIR  = 0o040000 # directory
    _IFCHR  = 0o020000 # character special
    _IFBLK  = 0o060000 # block special
    _IFREG  = 0o100000 # regular
    _IFLNK  = 0o120000 # symbolic link
    _IFSOCK = 0o140000 # socket
    _IFIFO  = 0o010000 # fifo

    S_BLKSIZE = 1024 # size of a block

    S_ISUID  = 0o004000 # set user id on execution
    S_ISGID  = 0o002000 # set group id on execution
    S_ISVTX  = 0o001000 # save swapped text even after use

    S_IREAD  = 0o000400 # read permission, owner
    S_IWRITE = 0o000200 # write permission, owner
    S_IEXEC  = 0o000100 # execute/search permission, owner
    S_ENFMT  = 0o002000 # enforcement-mode locking


    S_IFMT   = _IFMT
    S_IFDIR  = _IFDIR
    S_IFCHR  = _IFCHR
    S_IFBLK  = _IFBLK
    S_IFREG  = _IFREG
    S_IFLNK  = _IFLNK
    S_IFSOCK = _IFSOCK
    S_IFIFO  = _IFIFO


    # The Windows header files define _S_ forms of these, so we do too for easier portability.
    _S_IFMT   = _IFMT
    _S_IFDIR  = _IFDIR
    _S_IFCHR  = _IFCHR
    _S_IFIFO  = _IFIFO
    _S_IFREG  = _IFREG
    _S_IREAD  = 0o000400
    _S_IWRITE = 0o000200
    _S_IEXEC  = 0o000100


    S_IRUSR = 0o000400 # read permission, owner
    S_IWUSR = 0o000200 # write permission, owner
    S_IXUSR = 0o000100 # execute/search permission, owner
    S_IRWXU = (S_IRUSR | S_IWUSR | S_IXUSR)

    S_IRGRP = 0o000040 # read permission, group
    S_IWGRP = 0o000020 # write permission, grougroup
    S_IXGRP = 0o000010 # execute/search permission, group
    S_IRWXG = (S_IRGRP | S_IWGRP | S_IXGRP)
    S_IROTH = 0o000004 # read permission, other
    S_IWOTH = 0o000002 # write permission, other
    S_IXOTH = 0o000001 # execute/search permission, other
    S_IRWXO = (S_IROTH | S_IWOTH | S_IXOTH)


    # copied from https://github.com/bminor/newlib/blob/master/newlib/libc/sys/linux/sys/unistd.h

    SEEK_SET = 0
    SEEK_CUR = 1
    SEEK_END = 2

    STDIN_FILENO  = 0 # standard input file descriptor
    STDOUT_FILENO = 1 # standard output file descriptor
    STDERR_FILENO = 2 # standard error file descriptor

    # copied from https://github.com/bminor/newlib/blob/master/newlib/libc/include/sys/errno.h

    EPERM           = 1   # Not owner
    ENOENT          = 2   # No such file or directory
    ESRCH           = 3   # No such process
    EINTR           = 4   # Interrupted system call
    EIO             = 5   # I/O error
    ENXIO           = 6   # No such device or address
    E2BIG           = 7   # Arg list too long
    ENOEXEC         = 8   # Exec format error
    EBADF           = 9   # Bad file number
    ECHILD          = 10  # No children
    EAGAIN          = 11  # No more processes
    ENOMEM          = 12  # Not enough space
    EACCES          = 13  # Permission denied
    EFAULT          = 14  # Bad address
    ENOTBLK         = 15  # Block device required
    EBUSY           = 16  # Device or resource busy
    EEXIST          = 17  # File exists
    EXDEV           = 18  # Cross-device link
    ENODEV          = 19  # No such device
    ENOTDIR         = 20  # Not a directory
    EISDIR          = 21  # Is a directory
    EINVAL          = 22  # Invalid argument
    ENFILE          = 23  # Too many open files in system
    EMFILE          = 24  # File descriptor value too large
    ENOTTY          = 25  # Not a character device
    ETXTBSY         = 26  # Text file busy
    EFBIG           = 27  # File too large
    ENOSPC          = 28  # No space left on device
    ESPIPE          = 29  # Illegal seek
    EROFS           = 30  # Read-only file system
    EMLINK          = 31  # Too many links
    EPIPE           = 32  # Broken pipe
    EDOM            = 33  # Mathematics argument out of domain of function
    ERANGE          = 34  # Result too large
    ENOMSG          = 35  # No message of desired type
    EIDRM           = 36  # Identifier removed
    ECHRNG          = 37  # Channel number out of range
    EL2NSYNC        = 38  # Level 2 not synchronized
    EL3HLT          = 39  # Level 3 halted
    EL3RST          = 40  # Level 3 reset
    ELNRNG          = 41  # Link number out of range
    EUNATCH         = 42  # Protocol driver not attached
    ENOCSI          = 43  # No CSI structure available
    EL2HLT          = 44  # Level 2 halted
    EDEADLK         = 45  # Deadlock
    ENOLCK          = 46  # No lock
    EBADE           = 50  # Invalid exchange
    EBADR           = 51  # Invalid request descriptor
    EXFULL          = 52  # Exchange full
    ENOANO          = 53  # No anode
    EBADRQC         = 54  # Invalid request code
    EBADSLT         = 55  # Invalid slot
    EDEADLOCK       = 56  # File locking deadlock error
    EBFONT          = 57  # Bad font file fmt
    ENOSTR          = 60  # Not a stream
    ENODATA         = 61  # No data (for no delay io)
    ETIME           = 62  # Stream ioctl timeout
    ENOSR           = 63  # No stream resources
    ENONET          = 64  # Machine is not on the network
    ENOPKG          = 65  # Package not installed
    EREMOTE         = 66  # The object is remote
    ENOLINK         = 67  # Virtual circuit is gone
    EADV            = 68  # Advertise error
    ESRMNT          = 69  # Srmount error
    ECOMM           = 70  # Communication error on send
    EPROTO          = 71  # Protocol error
    EMULTIHOP       = 74  # Multihop attempted
    ELBIN           = 75  # Inode is remote (not really error)
    EDOTDOT         = 76  # Cross mount point (not really error)
    EBADMSG         = 77  # Bad message
    EFTYPE          = 79  # Inappropriate file type or format
    ENOTUNIQ        = 80  # Given log. name not unique
    EBADFD          = 81  # f.d. invalid for this operation
    EREMCHG         = 82  # Remote address changed
    ELIBACC         = 83  # Can't access a needed shared lib
    ELIBBAD         = 84  # Accessing a corrupted shared lib
    ELIBSCN         = 85  # .lib section in a.out corrupted
    ELIBMAX         = 86  # Attempting to link in too many libs
    ELIBEXEC        = 87  # Attempting to exec a shared library
    ENOSYS          = 88  # Function not implemented
    ENMFILE         = 89  # No more files
    ENOTEMPTY       = 90  # Directory not empty
    ENAMETOOLONG    = 91  # File or path name too long
    ELOOP           = 92  # Too many symbolic links
    EOPNOTSUPP      = 95  # Operation not supported on socket
    EPFNOSUPPORT    = 96  # Protocol family not supported
    ECONNRESET      = 104 # Connection reset by peer
    ENOBUFS         = 105 # No buffer space available
    EAFNOSUPPORT    = 106 # Address family not supported by protocol family
    EPROTOTYPE      = 107 # Protocol wrong type for socket
    ENOTSOCK        = 108 # Socket operation on non-socket
    ENOPROTOOPT     = 109 # Protocol not available
    ESHUTDOWN       = 110 # Can't send after socket shutdown
    ECONNREFUSED    = 111 # Connection refused
    EADDRINUSE      = 112 # Address already in use
    ECONNABORTED    = 113 # Software caused connection abort
    ENETUNREACH     = 114 # Network is unreachable
    ENETDOWN        = 115 # Network interface is not configured
    ETIMEDOUT       = 116 # Connection timed out
    EHOSTDOWN       = 117 # Host is down
    EHOSTUNREACH    = 118 # Host is unreachable
    EINPROGRESS     = 119 # Connection already in progress
    EALREADY        = 120 # Socket already connected
    EDESTADDRREQ    = 121 # Destination address required
    EMSGSIZE        = 122 # Message too long
    EPROTONOSUPPORT = 123 # Unknown protocol
    ESOCKTNOSUPPORT = 124 # Socket type not supported
    EADDRNOTAVAIL   = 125 # Address not available
    ENETRESET       = 126 # Connection aborted by network
    EISCONN         = 127 # Socket is already connected
    ENOTCONN        = 128 # Socket is not connected
    ETOOMANYREFS    = 129
    EPROCLIM        = 130
    EUSERS          = 131
    EDQUOT          = 132
    ESTALE          = 133
    ENOTSUP         = 134 # Not supported
    ENOMEDIUM       = 135 # No medium (in tape drive)
    ENOSHARE        = 136 # No such host or network path
    ECASECLASH      = 137 # Filename exists with different case
    EILSEQ          = 138 # Illegal byte sequence
    EOVERFLOW       = 139 # Value too large for defined data type
    ECANCELED       = 140 # Operation canceled
    ENOTRECOVERABLE = 141 # State not recoverable
    EOWNERDEAD      = 142 # Previous owner died
    ESTRPIPE        = 143 # Streams pipe error
    EWOULDBLOCK     = EAGAIN    # Operation would block

    __ELASTERROR = 2000 # Users can add values starting here


def map_file_mode(value, from_=Flags, to=stat):
    out = 0
    if value & from_.S_IRWXU:  out |= to.S_IREAD | to.S_IWRITE
    if value & from_.S_IRUSR:  out |= to.S_IREAD
    if value & from_.S_IWUSR:  out |= to.S_IWRITE
    if value & from_.S_IREAD:  out |= to.S_IREAD
    if value & from_.S_IWRITE: out |= to.S_IWRITE
    if value & from_.S_IRWXU:  out |= to.S_IRWXU
    if value & from_.S_IRUSR:  out |= to.S_IRUSR
    if value & from_.S_IWUSR:  out |= to.S_IWUSR
    if value & from_.S_IXUSR:  out |= to.S_IXUSR
    if value & from_.S_IRWXG:  out |= to.S_IRWXG
    if value & from_.S_IRGRP:  out |= to.S_IRGRP
    if value & from_.S_IWGRP:  out |= to.S_IWGRP
    if value & from_.S_IXGRP:  out |= to.S_IXGRP
    if value & from_.S_IRWXO:  out |= to.S_IRWXO
    if value & from_.S_IROTH:  out |= to.S_IROTH
    if value & from_.S_IWOTH:  out |= to.S_IWOTH
    if value & from_.S_IXOTH:  out |= to.S_IXOTH
    if value & from_.S_ISUID:  out |= to.S_ISUID
    if value & from_.S_ISGID:  out |= to.S_ISGID
    if value & from_.S_ISVTX:  out |= to.S_ISVTX
    if value & from_.S_IEXEC:  out |= to.S_IEXEC
    if value & from_.S_ENFMT:  out |= to.S_ENFMT
    if value & from_.S_IFMT:   out |= to.S_IFMT
    if value & from_.S_IFDIR:  out |= to.S_IFDIR
    if value & from_.S_IFCHR:  out |= to.S_IFCHR
    if value & from_.S_IFBLK:  out |= to.S_IFBLK
    if value & from_.S_IFREG:  out |= to.S_IFREG
    if value & from_.S_IFLNK:  out |= to.S_IFLNK
    if value & from_.S_IFSOCK: out |= to.S_IFSOCK
    if value & from_.S_IFIFO:  out |= to.S_IFIFO

    return out

def map_seek_flags(value, from_=Flags, to=os):
    out = 0
    if value & from_.SEEK_SET: out |= to.SEEK_SET;
    if value & from_.SEEK_CUR: out |= to.SEEK_CUR;
    if value & from_.SEEK_END: out |= to.SEEK_END;
    return out


def map_open_flags(value, from_=Flags, to=os):
    out = 0
    if hasattr(to, "O_BINARY"): out |= to.O_BINARY
    if value & from_.O_APPEND   : out |= to.O_APPEND
    if value & from_.O_CREAT    : out |= to.O_CREAT
    if value & from_.O_EXCL     : out |= to.O_EXCL
    if value & from_.O_RDONLY   : out |= to.O_RDONLY
    if value & from_.O_WRONLY   : out |= to.O_WRONLY
    if value & from_.O_RDWR     : out |= to.O_RDWR
    if value & from_.O_NOCTTY   : out |= to.O_NOCTTY
    if value & from_.O_NONBLOCK : out |= to.O_NONBLOCK
    if value & from_.O_SYNC     : out |= to.O_SYNC
    #if value & from_.O_ASYNC    : out |= to.O_ASYNC
    if value & from_.O_CLOEXEC  : out |= to.O_CLOEXEC
    if value & from_.O_DIRECT   : out |= to.O_DIRECT
    if value & from_.O_DIRECTORY: out |= to.O_DIRECTORY
    if value & from_.O_DSYNC    : out |= to.O_DSYNC
    #if value & from_.O_LARGEFILE: out |= to.O_LARGEFILE
    if value & from_.O_NOATIME  : out |= to.O_NOATIME
    if value & from_.O_NDELAY   : out |= to.O_NDELAY
    if value & from_.O_PATH     : out |= to.O_PATH
    if value & from_.O_TRUNC    : out |= to.O_TRUNC

    return out

def map_errno(value, from_=Flags, to=errno):
    codes = ['EPERM', 'ENOENT', 'ESRCH', 'EINTR', 'EIO', 'ENXIO', 'E2BIG', 'ENOEXEC', 'EBADF', 'ECHILD', 'EAGAIN', 'ENOMEM', 'EACCES', 'EFAULT', 'ENOTBLK',
             'EBUSY', 'EEXIST', 'EXDEV', 'ENODEV', 'ENOTDIR', 'EISDIR', 'EINVAL', 'ENFILE', 'EMFILE', 'ENOTTY', 'ETXTBSY', 'EFBIG', 'ENOSPC', 'ESPIPE',
             'EROFS', 'EMLINK', 'EPIPE', 'EDOM', 'ERANGE', 'ENOMSG', 'EIDRM', 'ECHRNG', 'EL2NSYNC', 'EL3HLT', 'EL3RST', 'ELNRNG', 'EUNATCH', 'ENOCSI',
             'EL2HLT', 'EDEADLK', 'ENOLCK', 'EBADE', 'EBADR', 'EXFULL', 'ENOANO', 'EBADRQC', 'EBADSLT', 'EDEADLOCK', 'EBFONT', 'ENOSTR', 'ENODATA', 'ETIME',
             'ENOSR', 'ENONET', 'ENOPKG', 'EREMOTE', 'ENOLINK', 'EADV', 'ESRMNT', 'ECOMM', 'EPROTO', 'EMULTIHOP', 'ELBIN', 'EDOTDOT', 'EBADMSG', 'EFTYPE',
             'ENOTUNIQ', 'EBADFD', 'EREMCHG', 'ELIBACC', 'ELIBBAD', 'ELIBSCN', 'ELIBMAX', 'ELIBEXEC', 'ENOSYS', 'ENMFILE', 'ENOTEMPTY', 'ENAMETOOLONG',
             'ELOOP', 'EOPNOTSUPP', 'EPFNOSUPPORT', 'ECONNRESET', 'ENOBUFS', 'EAFNOSUPPORT', 'EPROTOTYPE', 'ENOTSOCK', 'ENOPROTOOPT', 'ESHUTDOWN',
             'ECONNREFUSED', 'EADDRINUSE', 'ECONNABORTED', 'ENETUNREACH', 'ENETDOWN', 'ETIMEDOUT', 'EHOSTDOWN', 'EHOSTUNREACH', 'EINPROGRESS', 'EALREADY',
             'EDESTADDRREQ', 'EMSGSIZE', 'EPROTONOSUPPORT', 'ESOCKTNOSUPPORT', 'EADDRNOTAVAIL', 'ENETRESET', 'EISCONN', 'ENOTCONN', 'ETOOMANYREFS',
             'EPROCLIM', 'EUSERS', 'EDQUOT', 'ESTALE', 'ENOTSUP', 'ENOMEDIUM', 'ENOSHARE', 'ECASECLASH', 'EILSEQ', 'EOVERFLOW', 'ECANCELED', 'ENOTRECOVERABLE',
             'EOWNERDEAD', 'ESTRPIPE', 'EWOULDBLOCK']

    try:
        ec = next(ec for ec in codes if hasattr(from_, ec) and value == getattr(from_, ec))

        if not hasattr(to, ec):
            return to.EBADMSG

        return getattr(to, ec)
    except StopIteration:
        return to.EBADMSG

