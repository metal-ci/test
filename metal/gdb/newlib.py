import errno
import stat
import gdb
import os

from metal.gdb.metal_break import Breakpoint
from metal.newlib import Flags, map_errno, map_file_mode, map_open_flags


class FStat(Breakpoint):
    def __init__(self, os_=os):
        self.os_ = os_
        Breakpoint.__init__(self, "syscall.fstat")

    def stop(self, bp):
        fr = gdb.selected_frame()
        fd = next(int(str(arg.value(fr))) for arg in fr.block() if arg.is_argument)
        try:
            st = self.os_.fstat(fd)

            gdb.execute("set var st->st_dev   = {}".format(st.st_dev))
            gdb.execute("set var st->st_ino   = {}".format(st.st_ino))
            gdb.execute("set var st->st_mode  = {}".format(map_file_mode(st.st_mode, self.os_, Flags)))
            gdb.execute("set var st->st_nlink = {}".format(st.st_nlink))
            gdb.execute("set var st->st_uid   = {}".format(st.st_uid))
            gdb.execute("set var st->st_gid   = {}".format(st.st_gid))
            gdb.execute("set var st->st_size  = {}".format(st.st_size))

            gdb.execute("set var st->st_atim.tv_sec = {}".format(int(st.st_atime)))
            gdb.execute("set var st->st_mtim.tv_sec = {}".format(int(st.st_mtime)))
            gdb.execute("set var st->st_ctim.tv_sec = {}".format(int(st.st_ctime)))

            gdb.execute("set var st->st_atim.tv_nsec = {}".format((st.st_atime_ns or int(st.st_atime * 1000000000)) % 1000000000))
            gdb.execute("set var st->st_mtim.tv_nsec = {}".format((st.st_mtime_ns or int(st.st_mtime * 1000000000)) % 1000000000))
            gdb.execute("set var st->st_ctim.tv_nsec = {}".format((st.st_ctime_ns or int(st.st_ctime * 1000000000)) % 1000000000))

            if hasattr(st, 'st_rdev') and getattr(st, 'st_rdev') is not None:
                gdb.execute("set var st->st_rdev = {}".format(getattr(st, 'st_rdev')))
            if hasattr(st, 'st_blksize') and getattr(st, 'st_blksize') is not None:
                gdb.execute("set var st->st_blksize = {}".format(getattr(st, 'st_blksize')))
            if hasattr(st, 'st_blocks')  and getattr(st, 'st_blocks') is not None:
                gdb.execute("set var st->st_blocks = {}".format(getattr(st, 'st_blocks')))

            gdb.execute("set var res = 0")
            gdb.execute('set var err = 0')
        except OSError as e:
            gdb.execute("set var err = {}".format(map_errno(int(str(e)), errno, Flags)))


class Stat(Breakpoint):
    def __init__(self, os_=os):
        self.os_ = os_
        Breakpoint.__init__(self, "syscall.stat")

    def stop(self, bp):
        fr = gdb.selected_frame()
        file = next(str(arg.value(fr).string()) for arg in fr.block() if arg.is_argument)
        try:
            st = self.os_.stat(file)

            gdb.execute("set var st->st_dev   = {}".format(st.st_dev))
            gdb.execute("set var st->st_ino   = {}".format(st.st_ino))
            gdb.execute("set var st->st_mode  = {}".format(map_file_mode(st.st_mode, stat, Flags)))
            gdb.execute("set var st->st_nlink = {}".format(st.st_nlink))
            gdb.execute("set var st->st_uid   = {}".format(st.st_uid))
            gdb.execute("set var st->st_gid   = {}".format(st.st_gid))
            gdb.execute("set var st->st_rdev  = {}".format(st.st_rdev))
            gdb.execute("set var st->st_size  = {}".format(st.st_size))

            gdb.execute("set var st->st_atime.tv_sec = {}".format(int(st.st_atime)))
            gdb.execute("set var st->st_mtime.tv_sec = {}".format(int(st.st_mtime)))
            gdb.execute("set var st->st_ctime.tv_sec = {}".format(int(st.st_ctime)))

            gdb.execute("set var st->st_atime.tv_nsec = {}".format(st.st_atime_ns % 1000000000))
            gdb.execute("set var st->st_mtime.tv_nsec = {}".format(st.st_mtime_ns % 1000000000))
            gdb.execute("set var st->st_ctime.tv_nsec = {}".format(st.st_ctime_ns % 1000000000))

            if hasattr(st, 'st_rdev'):    gdb.execute("set var st->st_rdev = {}".format(getattr(st, 'st_rdev')))
            if hasattr(st, 'st_blksize'): gdb.execute("set var st->st_blksize = {}".format(getattr(st, 'st_blksize')))
            if hasattr(st, 'st_blocks'):  gdb.execute("set var st->st_blocks = {}".format(getattr(st, 'st_blocks')))

            gdb.execute("set var res = 0")
            gdb.execute('set var err = 0')
        except OSError as e:
            gdb.execute("set var err = {}".format(map_errno(int(str(e)), errno, Flags)))


class IsAtty(Breakpoint):
    def __init__(self, os_=os):
        self.os_ = os_
        Breakpoint.__init__(self, "syscall.isatty")

    def stop(self, bp):
        fr = gdb.selected_frame()
        fd = next(int(str(arg.value(fr))) for arg in fr.block() if arg.is_argument)
        try:
            gdb.execute("set var res = {}".format(1 if self.os_.isatty(fd) else 0))
            gdb.execute('set var err = 0')
        except OSError as e:
            gdb.execute("set var err = {}".format(map_errno(int(str(e)), errno, Flags)))


class Link(Breakpoint):
    def __init__(self, os_=os):
        self.os_ = os_
        Breakpoint.__init__(self, "syscall.link")

    def stop(self, bp):
        fr = gdb.selected_frame()
        [existing, new_] = [str(arg.value(fr).string()) for arg in fr.block() if arg.is_argument]
        try:
            self.os_.link(existing, new_)
            gdb.execute("set var res = 0")
            gdb.execute('set var err = 0')
        except OSError as e:
            gdb.execute("set var err = {}".format(map_errno(int(str(e)), errno, Flags)))


class Symlink(Breakpoint):
    def __init__(self, os_=os):
        self.os_ = os_
        Breakpoint.__init__(self, "syscall.symlink")

    def stop(self, bp):
        fr = gdb.selected_frame()
        [existing, new_] = [str(arg.value(fr).string()) for arg in fr.block() if arg.is_argument]
        try:
            self.os_.symlink(existing, new_)
            gdb.execute("set var res = 0")
            gdb.execute('set var err = 0')
        except OSError as e:
            gdb.execute("set var err = {}".format(map_errno(int(str(e)), errno, Flags)))


class Unlink(Breakpoint):
    def __init__(self, os_=os):
        self.os_ = os_
        Breakpoint.__init__(self, "syscall.unlink")

    def stop(self, bp):
        fr = gdb.selected_frame()
        name = next(str(arg.value(fr).string()) for arg in fr.block() if arg.is_argument)
        try:
            gdb.execute("set var res = {}".format(self.os_.unlink(name)))
            gdb.execute('set var err = 0')
        except OSError as e:
            gdb.execute("set var err = {}".format(map_errno(int(str(e)), errno, Flags)))


class Open(Breakpoint):
    def __init__(self, os_=os):
        self.os_ = os_
        Breakpoint.__init__(self, "syscall.open")

    def stop(self, bp):
        fr = gdb.selected_frame()
        itr = (arg.value(fr) for arg in fr.block() if arg.is_argument)
        file = str(next(itr).string())
        flags = map_open_flags(int(str(next(itr))), Flags, self.os_)
        mode = map_file_mode(int(str(next(itr))), Flags, self.os_)

        try:
            gdb.execute("set var res = {}".format(self.os_.open(file, flags, mode)))
            gdb.execute('set var err = 0')
        except OSError as e:
            gdb.execute("set var err = {}".format(map_errno(int(str(e)), errno, Flags)))


class LSeek(Breakpoint):
    def __init__(self, os_=os):
        self.os_ = os_
        Breakpoint.__init__(self, "syscall.lseek")

    def stop(self, bp):
        fr = gdb.selected_frame()
        file, ptr, dir_ = (arg.value(fr) for arg in fr.block() if arg.is_argument)

        try:
            gdb.execute("set var res = {}".format(self.os_.lseek(file, ptr, dir_)))
            gdb.execute('set var err = 0')
        except OSError as e:
            gdb.execute("set var err = {}".format(map_errno(int(str(e)), errno, Flags)))


class Write(Breakpoint):
    def __init__(self, os_=os):
        self.os_ = os_
        Breakpoint.__init__(self, "syscall.write")

    def stop(self, bp):
        fr = gdb.selected_frame()

        block = fr.block()
        while block.function is None:
            block = block.superblock

        file, ptr, len_ = (arg.value(fr) for arg in block if arg.is_argument)

        try:
            buf = gdb.selected_inferior().read_memory(ptr,  len_)
            gdb.execute("set var res = {}".format(self.os_.write(file, buf.tobytes())))
            gdb.execute("set var err = 0")
        except OSError as e:
            gdb.execute("set var err = {}".format(map_errno(int(str(e)), errno, Flags)))


class Read(Breakpoint):
    def __init__(self, os_=os):
        self.os_ = os_
        Breakpoint.__init__(self, "syscall.read")

    def stop(self, bp):
        fr = gdb.selected_frame()
        b = fr.block()
        while b.function is None:
            b = b.superblock

        arg_values = (arg.value(fr) for arg in b if arg.is_argument)

        file = int(str(next(arg_values)))
        ptr = int(next(arg_values))
        len_ = int(str(next(arg_values)))

        try:
            buf = self.os_.read(file, len_)
            gdb.selected_inferior().write_memory(ptr, buf, len(buf))
            gdb.execute("set var res = {}".format(len(buf)))
            gdb.execute('set var err = 0')
        except OSError as e:
            gdb.execute("set var err = {}".format(map_errno(int(str(e)), errno, Flags)))


class ReadAvailable(Breakpoint):
    def __init__(self, os_=os):
        self.os_ = os_
        Breakpoint.__init__(self, "syscall.read_available")

    def stop(self, bp):
        fr = gdb.selected_frame()
        gb = fr.block().static_block

        file = next(int(str(arg.value(fr))) for arg in gb if arg.name == "read_fd")
        len_ = next(int(str(arg.value(fr))) for arg in fr.block() if arg.name == "buf_size")
        ptr = next(int(arg.value(fr).address) for arg in gb if arg.name == "read_buf")

        try:
            if self.os_.isatty(file):
                gdb.execute("set.var read_end = 0")  # No reading for terminal
                return

            cur = self.os_.lseek(file, 0, self.os_.SEEK_CUR)
            end = self.os_.lseek(file, 0, self.os_.SEEK_END)

            available = end - cur
            self.os_.lseek(file, cur, self.os_.SEEK_SET)
            read_len = min(available, len_)

            buf = self.os_.read(file, read_len)
            gdb.selected_inferior().write_memory(ptr, buf, len(buf))
            gdb.execute("set var read_end = {}".format(len(buf)))
        except OSError as e:
            gdb.execute("set var err = {}".format(map_errno(int(str(e)), errno, Flags)))


class Close(Breakpoint):
    def __init__(self, os_=os):
        self.os_ = os_
        Breakpoint.__init__(self, "syscall.close")

    def stop(self, bp):
        fr = gdb.selected_frame()
        fd = next(int(str(arg.value(fr))) for arg in fr.block() if arg.is_argument)

        try:
            if fd == Flags.STDERR_FILENO or fd == Flags.STDOUT_FILENO or fd == Flags.STDIN_FILENO:
                gdb.execute("set var err = {}".format(Flags.EACCES))
            else:
                self.os_.close(fd)
                gdb.execute("set var res = 0")
                gdb.execute('set var err = 0')
        except OSError as e:
            gdb.execute("set var err = {}".format(map_errno(int(str(e)), errno, Flags)))


class NewlibBreakpoints:
    def __init__(self, os_=os):
        self.fstat = FStat(os_)
        self.stat_ = Stat(os_)
        self.is_atty = IsAtty(os_)
        self.link = Link(os_)
        self.symlink = Symlink(os_)
        self.unlink = Unlink(os_)
        self.open_ = Open(os_)
        self.lseek = LSeek(os_)
        self.write = Write(os_)
        self.read = Read(os_)
        self.read_available = ReadAvailable(os_)
        self.close_ = Close(os_)
