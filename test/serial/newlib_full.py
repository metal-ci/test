import argparse
import errno
import os

from metal.serial import Engine, Exit
from subprocess import PIPE, Popen

from metal.serial.generate import generate

from metal.serial.newlib import build_newlib_hook

parser = argparse.ArgumentParser()

parser.add_argument('binary',           help='The binary that runs on target')
parser.add_argument('-S', '--source-dir',  required=True, help='The root of the source directory')
parser.add_argument('-I', '--include', nargs='+', help="Include folders for the preprocessor", default=[])
parser.add_argument('-D', '--define', nargs='+', help="Defines for the preprocessor", default=[])

args = parser.parse_args()

serial_info = generate(args.binary, args.define, args.include)

p = Popen(args.binary, stdin=PIPE, stdout=PIPE, close_fds=True)

class os_stub:
    stat_result = os.stat_result
    O_WRONLY = 1
    O_APPEND = 2
    O_CREAT  = 4
    O_EXCL   = 5
    O_NOINHERIT = 6
    O_RANDOM = 7
    O_RDONLY = 8
    O_RDWR   = 9
    O_SEQUENTIAL = 10
    O_NOCTTY = 11
    O_NONBLOCK = 12
    O_SYNC = 13
    O_CLOEXEC = 14

    O_DIRECT = 15
    O_DIRECTORY = 16
    O_DSYNC = 17

    O_NOATIME = 18
    O_NDELAY = 19
    O_PATH = 20
    O_TRUNC = 21

    O_READ = 22
    O_WRITE = 23
    O_RDWR = 24

    SEEK_SET = 42
    SEEK_CUR = 43
    SEEK_END = 44

    S_IREAD   = 1
    S_IWRITE  = 2
    S_IREAD   = 3
    S_IWRITE  = 4
    S_IRWXU   = 5
    S_IRUSR   = 6
    S_IWUSR   = 7
    S_IXUSR   = 8
    S_IRWXG   = 9
    S_IRGRP   = 10
    S_IWGRP   = 11
    S_IXGRP   = 12
    S_IRWXO   = 13
    S_IROTH   = 14
    S_IWOTH   = 15
    S_IXOTH   = 16
    S_ISUID   = 17
    S_ISGID   = 18
    S_ISVTX   = 19
    S_IEXEC   = 10
    S_ENFMT   = 21
    S_IFMT    = 22
    S_IFDIR   = 23
    S_IFCHR   = 24
    S_IFBLK   = 25
    S_IFREG   = 26
    S_IFLNK   = 27
    S_IFSOCK  = 28
    S_IFIFO   = 29

    def __init__(self):
        self.write_cnt = 0
        self.open_cnt = 0
        self.close_cnt = 0
        self.fds = [1, 2]

    def write(self, fd, msg):
        assert fd in self.fds
        if fd == 1:
            assert msg == b"Writing stdout\n"
        if fd == 2:
            assert msg == b"Writing stderr\n"
        if fd == 3:
            assert msg == b"Writing to fd_\n"

        self.write_cnt = self.write_cnt + 1
        return len(msg)

    def open(self, filename, flags, mode):
        assert filename == "test-file"
        assert flags & os_stub.O_RDWR
        assert mode == 0
        self.open_cnt  = self.open_cnt + 1

        self.fds.append(3)
        return 3

    def close(self, fd):
        assert fd == 3
        self.close_cnt = self.close_cnt + 1

    def read(self, fd, n):
        assert n == 5
        if fd == 0:
            return b'stdin'
        elif fd == 3:
            return b'testf'
        else:
            assert False

    def stat(self, name):
        assert name.endswith('newlib_full.c')
        raise OSError(errno.ENOENT)

    def fstat(self, name):
        st = os.stat_result((
            3, 2, 1, 4, 5, 6, 1024, 900.000000800, 3000, 5000
            ))

        return st

    def isatty(self, fd):
        if fd == 1:
            return False
        if fd == 2:
            return True

    def link(self, existing, new):
        assert existing.endswith('syscalls.h')
        assert new.endswith('lib/syscalls.c')
        return 0

    def symlink(self, existing, new):
        assert existing.endswith("doesn't exist")
        assert new.endswith('lib/syscalls.h')
        raise OSError(errno.ENOENT)

    def unlink(self, existing):
        assert existing.endswith('syscalls.h')
        return 0

    def lseek(self, fd, ptr, dir):
        assert fd in [0, 3]
        assert ptr == 0

        if dir == os_stub.SEEK_CUR:
            return 0
        if dir == os_stub.SEEK_END:
            return 5




oss = os_stub()
engine = Engine(input=p.stdout, output=p.stdin, serial_info=serial_info,
                macro_hooks=[Exit, build_newlib_hook(oss)])

assert engine.init_marker.file.endswith('newlib_full.c')
assert engine.run() == 0
assert oss.write_cnt == 3
assert oss.open_cnt == 1