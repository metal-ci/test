import argparse
import os

from metal.cpputest import CppUTestOutput
from metal.serial import Engine, Exit
from subprocess import PIPE, Popen

from metal.serial.cpputest import CppUTest
from metal.serial.generate import generate

from metal.serial.newlib import build_newlib_hook

parser = argparse.ArgumentParser()

parser.add_argument('binary',           help='The binary that runs on target')
parser.add_argument('-S', '--source-dir',  required=True, help='The root of the source directory')
parser.add_argument('-I', '--include', nargs='+', help="Include folders for the preprocessor", default=[])
parser.add_argument('-D', '--define', nargs='+', help="Defines for the preprocessor", default=[])

args = parser.parse_args()

serial_info = generate(args.binary, args.define, args.include, ['METAL_SERIAL_CPPUTEST'])

p = Popen(args.binary, stdin=PIPE, stdout=PIPE, close_fds=True)


class TestOutput(CppUTestOutput):
    def __init__(self):
        super().__init__()


testOutput = TestOutput()

engine = Engine(input=p.stdout, output=p.stdin, serial_info=serial_info,
                macro_hooks=[Exit, lambda: CppUTest(testOutput)])

assert engine.init_marker.file.endswith('cpputest.cpp')
assert engine.run() == 1
