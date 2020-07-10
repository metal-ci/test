import argparse
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

    def open(self, filename, flags, mode):
        assert filename == "test-file"
        assert flags == os_stub.O_WRONLY
        assert mode == 0
        self.open_cnt  = self.open_cnt + 1

        self.fds.append(3)
        return 3

    def close(self, fd):
        assert fd == 3
        self.close_cnt = self.close_cnt + 1

oss = os_stub()
engine = Engine(input=p.stdout, output=p.stdin, serial_info=serial_info,
                macro_hooks=[Exit, build_newlib_hook(oss)])

assert engine.init_marker.file.endswith('newlib_unchecked.c')
assert engine.run() == 0
assert oss.write_cnt == 3
assert oss.open_cnt == 1