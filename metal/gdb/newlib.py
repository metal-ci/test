import errno
import stat
import traceback

import gdb
import os

from metal.gdb import Breakpoint
from metal.newlib import Flags, map_errno, map_file_mode, map_open_flags


class FStat(Breakpoint):
    def __init__(self):
        Breakpoint.__init__(self, "syscall.fstat")

    def stop(self, bp):
        fr = gdb.selected_frame()
        fd = next(int(str(arg.value())) for arg in fr.block() if arg.is_argument)
        try:
            st = os.fstat(fd)

            gdb.execute("set var st->st_dev   = {}", st.st_dev)
            gdb.execute("set var st->st_ino   = {}", st.st_ino)
            gdb.execute("set var st->st_mode  = {}", map_file_mode(st.st_mode, stat, Flags))
            gdb.execute("set var st->st_nlink = {}", st.st_nlink)
            gdb.execute("set var st->st_uid   = {}", st.st_uid)
            gdb.execute("set var st->st_gid   = {}", st.st_gid)
            gdb.execute("set var st->st_rdev  = {}", st.st_rdev)
            gdb.execute("set var st->st_size  = {}", st.st_size)

            gdb.execute("set var st->st_atime.tv_sec = {}", st.st_atime)
            gdb.execute("set var st->st_mtime.tv_sec = {}", st.st_mtime)
            gdb.execute("set var st->st_ctime.tv_sec = {}", st.st_ctime)

            gdb.execute("set var st->st_atime.tv_nsec = {}", st.st_atime_ns % 1000000000)
            gdb.execute("set var st->st_mtime.tv_nsec = {}", st.st_mtime_ns % 1000000000)
            gdb.execute("set var st->st_ctime.tv_nsec = {}", st.st_ctime_ns % 1000000000)

            gdb.execute("set var res = 0")
        except OSError as e:
            gdb.execute("set var err = ".format(map_errno(e.errno, errno, Flags)))


fstat = FStat()


class Stat(Breakpoint):
    def __init__(self):
        Breakpoint.__init__(self, "syscall.stat")

    def stop(self, bp):
        fr = gdb.selected_frame()
        file = next(str(arg.value()) for arg in fr.block() if arg.is_argument)
        try:
            st = os.stat(file)

            gdb.execute("set var st->st_dev   = {}", st.st_dev)
            gdb.execute("set var st->st_ino   = {}", st.st_ino)
            gdb.execute("set var st->st_mode  = {}", map_file_mode(st.st_mode, stat, Flags))
            gdb.execute("set var st->st_nlink = {}", st.st_nlink)
            gdb.execute("set var st->st_uid   = {}", st.st_uid)
            gdb.execute("set var st->st_gid   = {}", st.st_gid)
            gdb.execute("set var st->st_rdev  = {}", st.st_rdev)
            gdb.execute("set var st->st_size  = {}", st.st_size)

            gdb.execute("set var st->st_atime.tv_sec = {}", st.st_atime)
            gdb.execute("set var st->st_mtime.tv_sec = {}", st.st_mtime)
            gdb.execute("set var st->st_ctime.tv_sec = {}", st.st_ctime)

            gdb.execute("set var st->st_atime.tv_nsec = {}", st.st_atime_ns % 1000000000)
            gdb.execute("set var st->st_mtime.tv_nsec = {}", st.st_mtime_ns % 1000000000)
            gdb.execute("set var st->st_ctime.tv_nsec = {}", st.st_ctime_ns % 1000000000)

            gdb.execute("set var res = 0")
        except OSError as e:
            gdb.execute("set var err = ".format(map_errno(e.errno, errno, Flags)))


stat_ = Stat()


class IsAtty(Breakpoint):
    def __init__(self):
        Breakpoint.__init__(self, "syscall.isatty")

    def stop(self, bp):
        fr = gdb.selected_frame()
        fd = next(int(str(arg.value())) for arg in fr.block() if arg.is_argument)
        try:
            gdb.execute("set var res = {}".format(os.isatty(fd)))
        except OSError as e:
            gdb.execute("set var err = ".format(map_errno(e.errno, errno, Flags)))


isAtty = IsAtty()


class Link(Breakpoint):
    def __init__(self):
        Breakpoint.__init__(self, "syscall.link")

    def stop(self, bp):
        fr = gdb.selected_frame()
        [existing, new_] = [str(arg.value()) for arg in fr.block() if arg.is_argument]
        try:
            os.link(existing, new_)
            gdb.execute("set var res = 0")
        except OSError as e:
            gdb.execute("set var err = ".format(map_errno(e.errno, errno, Flags)))


link = Link()


class Symlink(Breakpoint):
    def __init__(self):
        Breakpoint.__init__(self, "syscall.symlink")

    def stop(self, bp):
        fr = gdb.selected_frame()
        [existing, new_] = [str(arg.value()) for arg in fr.block() if arg.is_argument]
        try:
            os.symlink(existing, new_)
            gdb.execute("set var res = 0")
        except OSError as e:
            gdb.execute("set var err = ".format(map_errno(e.errno, errno, Flags)))


symlink = Symlink()


class Unlink(Breakpoint):
    def __init__(self):
        Breakpoint.__init__(self, "syscall.unlink")

    def stop(self, bp):
        fr = gdb.selected_frame()
        name = next(str(arg.value()) for arg in fr.block() if arg.is_argument)
        try:
            gdb.execute("set var res = {}".format(os.unlink(name)))
        except OSError as e:
            gdb.execute("set var err = ".format(map_errno(e.errno, errno, Flags)))


unlink = Unlink()


class Open(Breakpoint):
    def __init__(self):
        Breakpoint.__init__(self, "syscall.open")

    def stop(self, bp):
        fr = gdb.selected_frame()
        itr = (arg.value() for arg in fr.block() if arg.is_argument)
        file = str(next(itr))
        flags = map_open_flags(int(str(next(itr))))
        mode = map_file_mode(int(str(next(itr))))

        try:
            gdb.execute("set var res = {}".format(os.open(file, flags, mode)))
        except OSError as e:
            gdb.execute("set var err = ".format(map_errno(e.errno, errno, Flags)))


open_ = Open()


class LSeek(Breakpoint):
    def __init__(self):
        Breakpoint.__init__(self, "syscall.lseek")

    def stop(self, bp):
        fr = gdb.selected_frame()
        file, ptr, dir = (arg.value() for arg in fr.block() if arg.is_argument)

        try:
            gdb.execute("set var res = {}".format(os.lseek(file, ptr, dir)))
        except OSError as e:
            gdb.execute("set var err = ".format(map_errno(e.errno, errno, Flags)))


lseek = LSeek()


class Write(Breakpoint):
    def __init__(self):
        Breakpoint.__init__(self, "syscall.read")

    def stop(self, bp):
        fr = gdb.selected_frame()
        file, ptr, len_ = (arg.value() for arg in fr.block() if arg.is_argument)

        try:
            buf = gdb.selected_inferior().read_memory(ptr, ptr, len_)
            gdb.execute("set var res = {}".format(os.write(file, buf)))
        except OSError as e:
            gdb.execute("set var err = ".format(map_errno(e.errno, errno, Flags)))


write = Write()


class Read(Breakpoint):
    def __init__(self):
        Breakpoint.__init__(self, "syscall.read")

    def stop(self, bp):
        fr = gdb.selected_frame()
        file, ptr, len_ = (arg.value() for arg in fr.block() if arg.is_argument)

        try:
            buf = os.read(file, len_)
            gdb.selected_inferior().write_memory(ptr, buf, len(buf))
            gdb.execute("set var res = {}".format(len(buf)))
        except OSError as e:
            gdb.execute("set var err = ".format(map_errno(e.errno, errno, Flags)))


read = Read()


class ReadAvailable(Breakpoint):
    def __init__(self):
        Breakpoint.__init__(self, "syscall.read_available")

    def stop(self, bp):
        fr = gdb.selected_frame()
        file, ptr, len_ = (arg.value() for arg in fr.block() if arg.is_argument)

        try:
            if os.isatty(file):
                gdb.execute("set.var res = 0")  # No reading for terminal
                return

            cur = os.lseek(file, 0, os.SEEK_CUR)
            end = os.lseek(file, 0, os.SEEK_END)

            available = end - cur
            os.lseek(file, cur, os.SEEK_SET)
            read_len = min(available, len_)

            buf = os.read(file, read_len)
            gdb.selected_inferior().write_memory(ptr, buf, len(buf))
            gdb.execute("set var res = {}".format(len(buf)))
        except OSError as e:
            gdb.execute("set var err = ".format(map_errno(e.errno, errno, Flags)))


read_available = ReadAvailable()


class Close(Breakpoint):
    def __init__(self):
        Breakpoint.__init__(self, "syscall.close")

    def stop(self, bp):
        fr = gdb.selected_frame()
        fd = next(arg.value() for arg in fr.block() if arg.is_argument)

        try:
            if fd == Flags.STDERR_FILENO or fd == Flags.STDOUT_FILENO or fd == Flags.STDIN_FILENO:
                gdb.execute("set var err = ".format(Flags.EACCES))
            else:
                gdb.execute("set var res = {}".format(os.close(fd)))
        except OSError as e:
            gdb.execute("set var err = ".format(map_errno(e.errno, errno, Flags)))


close_ = Close()