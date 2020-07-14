import errno
import stat
import gdb
import os
import re
import sys

from metal.gdb.metal_break import Breakpoint
from metal.newlib import Flags, map_errno, map_file_mode, map_open_flags


class ArgvBreakpoint(Breakpoint):
    def __init__(self):
        Breakpoint.__init__(self, "argv")

    def stop(self, bp):
        res = gdb.execute('show args', to_string=True)
        args = [gdb.current_progspace().filename]
        try:
            arg_str = str(next(re.finditer('"((?:\\"|[^\"])*)"', res))[1])
            args.extend(re.split('(?<!\\\\) ', arg_str))
        except StopIteration:
            pass

        fr = gdb.selected_frame()

        ptr_size = int(str(gdb.parse_and_eval('sizeof(char*)')))
        buffer_address = 0
        buffer_size = 0
        try:
            buffer_address = int(str(gdb.parse_and_eval('&argv_buffer')))
            buffer_size = int(str(gdb.parse_and_eval('sizeof(argv_buffer)')))
        except:
            buffer_size = sum(len(arg) + 1 + ptr_size for arg in args)
            buffer_address = int(str(gdb.parse_and_eval('malloc({})'.format(buffer_size))), 16)

        used_args = 0

        needed_size = 0
        for arg in args:
            nsize = needed_size + ptr_size + len(arg.encode()) + 1
            if nsize > buffer_size:
                print("***metal.gdb***: Couldn't write all of argv, buffer size was {}".format(buffer_size), file=sys.stderr)
                args = args[used_args:]

            needed_size = nsize
            used_args = used_args + 1

        endian = 'little' if gdb.execute('show endian', to_string=True).find('little') != -1 else 'big'
        data_offset = buffer_address + (ptr_size * used_args)

        data = bytes()
        for arg in args:
            data = data + data_offset.to_bytes(ptr_size, endian)
            data_offset = data_offset + len(arg.encode()) + 1

        data = data + b''.join(arg.encode() + b'\x00' for arg in args)

        assert len(data) <= buffer_size

        gdb.selected_inferior().write_memory(buffer_address, data)
        gdb.parse_and_eval('argc = {}'.format(len(args)))
        gdb.parse_and_eval('argv = (char**){}'.format(buffer_address))