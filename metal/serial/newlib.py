import errno
import os
import stat
import sys
import typing
from os import stat_result

from metal.newlib import Flags, map_errno, map_open_flags, map_file_mode
from metal.serial import Engine
from metal.serial.hooks import MacroHook
from metal.serial.preprocessor import MacroExpansion


def write_stat(engine: Engine, st: stat_result):
    engine.write_int(st.st_dev)
    engine.write_int(st.st_ino)
    engine.write_int(map_file_mode(st.st_mode))
    engine.write_int(st.st_nlink)
    engine.write_int(st.st_uid)
    engine.write_int(st.st_gid)
    engine.write_int(st.st_rdev)
    engine.write_int(st.st_size)
    engine.write_int(st.st_blksize)
    engine.write_int(st.st_blocks)

    engine.write_int(int(st.st_atime))
    engine.write_int(st.st_atime_ns % 1000000000)
    engine.write_int(int(st.st_mtime))
    engine.write_int(st.st_mtime_ns % 1000000000)
    engine.write_int(int(st.st_ctime))
    engine.write_int(st.st_ctime_ns % 1000000000)


def fstat(engine: Engine):
    try:
        fd = engine.read_int()
        st = os.fstat(fd)
        engine.write_int(0)
        write_stat(engine, st)
    except OSError as e:
        engine.write_int(map_errno(e.errno, errno, Flags))


def stat_(engine: Engine):
    try:
        file = engine.read_string()
        st = os.stat(file)
        engine.write_int(0)
        write_stat(engine, st)
    except OSError as e:
        engine.write_int(map_errno(e.errno, errno, Flags))


def isatty(engine: Engine):
    try:
        fd = engine.read_int()
        isatty_ = os.isatty(fd)
        engine.write_int(0)
        engine.write_int(isatty_)
    except OSError as e:
        engine.write_int(map_errno(e.errno, errno, Flags))


def link(engine: Engine):
    try:
        existing = engine.read_string()
        _new = engine.read_string()
        os.link(existing, _new)
        engine.write_int(0)
    except OSError as e:
        engine.write_int(map_errno(e.errno, errno, Flags))


def symlink(engine: Engine):
    try:
        existing = engine.read_string()
        _new = engine.read_string()
        os.symlink(existing, _new)
        engine.write_int(0)
    except OSError as e:
        engine.write_int(map_errno(e.errno, errno, Flags))


def unlink(engine: Engine):
    try:
        name = engine.read_string()
        os.unlink(name)
        engine.write_int(0)
    except OSError as e:
        engine.write_int(map_errno(e.errno, errno, Flags))


def lseek(engine: Engine):
    try:
        file = engine.read_int()
        ptr = engine.read_int()
        dir_ = engine.read_int()
        engine.write_int(os.lseek(file, ptr, dir_))
    except OSError as e:
        engine.write_int(-1)
        engine.write_int(map_errno(e.errno, errno, Flags))


def open_full(engine: Engine):
    try:
        file = engine.read_string()
        flags = map_open_flags(engine.read_int())
        mode = map_file_mode(engine.read_int())

        engine.write_int(os.open(file, flags, mode))
    except OSError as e:
        engine.write_int(-1)
        engine.write_int(map_errno(e.errno, errno, Flags))


unchecked_map: typing.Dict[int, int] = {}


def open_unchecked(engine: Engine):
    file = engine.read_string()
    try:
        flags = map_open_flags(engine.read_int())
        mode = map_file_mode(engine.read_int())
        target_fd = engine.read_int()
        unchecked_map[target_fd] = os.open(file, flags, mode)
    except OSError as e:
        print("Error opening file {} : {}".format(file, e), file=sys.stderr)


def open_(engine: Engine, tp: str):
    if tp == 'full':
        open_full(engine)
    elif tp == 'unchecked':
        open_unchecked(engine)


def close_full(engine: Engine):
    try:
        fd = engine.read_int()
        os.close(fd)
        engine.write_int(0)
    except OSError as e:
        engine.write_int(-1)
        engine.write_int(map_errno(e.errno, errno, Flags))


def close_unchecked(engine: Engine):
    target_fd = engine.read_int()
    try:
        os.close(unchecked_map[target_fd])
    except OSError as e:
        print("Error closing file {} : {}".format(target_fd, e), file=sys.stderr)
    except KeyError:
        pass


def close_(engine: Engine, tp: str):
    if tp == 'full':
        close_full(engine)
    elif tp == 'unchecked':
        close_unchecked(engine)


def write_full(engine: Engine):
    try:
        fd = engine.read_int()
        dt = engine.read_memory()
        os.write(fd, dt)
    except OSError as e:
        engine.write_int(-1)
        engine.write_int(map_errno(e.errno, errno, Flags))


def write_unchecked(engine: Engine):
    fd = engine.read_int()
    dt = engine.read_memory()
    os.write(fd, dt)


def write(engine: Engine, tp: str):

    if tp == 'full':
        write_full(engine)
    elif tp == 'unchecked':
        write_unchecked(engine)


def read_full(engine: Engine):
    try:
        fd = engine.read_int()
        len_ = engine.read_int()
        buf = os.read(fd, len_)
        engine.write_int(0)
        engine.write_memory(buf)
    except OSError as e:
        engine.write_int(map_errno(e.errno, errno, Flags))


def read_buffered(engine: Engine):
    try:
        fd = engine.read_int()
        len_ = engine.read_int()

        cur = os.lseek(fd, 0, os.SEEK_CUR)
        end = os.lseek(fd, 0, os.SEEK_END)

        available = end - cur
        read_len = min(available, len_)

        buf = os.read(fd, read_len)
        engine.write_int(0)
        engine.write_memory(buf)
    except OSError as e:
        engine.write_int(map_errno(e.errno, errno, Flags))


def read(engine: Engine, tp: str):
    if tp == 'full':
        read_full(engine)
    elif tp == 'buffered':
        read_buffered(engine)


func_map = {
    "fstat": fstat,
    "stat": stat_,
    "isatty": isatty,
    "link": link,
    "symlink": symlink,
    "unlink": unlink,
    "lseek": lseek,
    "open": open_,
    "close": close_,
    "write": write,
    "read": read
}


class Syscall(MacroHook):
    identifier = 'METAL_SERIAL_SYSCALL'
    exit_code: typing.Optional[int]

    def invoke(self, engine: Engine,  macro_expansion: MacroExpansion):
        func = macro_expansion.args[0]
        spec = macro_expansion.args[1] if len(macro_expansion.args) > 1 else None

        try:
            if spec is None:
                func_map[func](engine)
            else:
                func_map[func](engine, spec)
        except KeyError:
            raise Exception("Function {} not found for syscalls".format(func))

    def __init__(self):
        super().__init__()


