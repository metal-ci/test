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

    def __init__(self):
        self.cnt = 0

    def write(self, fd, msg):
        assert fd in [1,2]
        if fd == 1:
            assert fd == 1
            assert msg == b"Writing stdout\n"
        if fd == 2:
            assert fd == 2
            assert msg == b"Writing stderr\n"

        self.cnt = self.cnt + 1



oss = os_stub()
engine = Engine(input=p.stdout, output=p.stdin, serial_info=serial_info,
                macro_hooks=[Exit, build_newlib_hook(oss)])

assert engine.init_marker.file.endswith('newlib_blocked.c')
assert engine.run() == 0
assert oss.cnt == 2