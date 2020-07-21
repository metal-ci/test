import argparse
import errno
import os

from metal.serial import Engine, Exit, MacroHook
from subprocess import PIPE, Popen

from metal.serial.generate import generate

from metal.serial.preprocessor import MacroExpansion
from metal.serial.unit import Unit

parser = argparse.ArgumentParser()

parser.add_argument('binary',           help='The binary that runs on target')
parser.add_argument('-S', '--source-dir',  required=True, help='The root of the source directory')
parser.add_argument('-I', '--include', nargs='+', help="Include folders for the preprocessor", default=[])
parser.add_argument('-D', '--define', nargs='+', help="Defines for the preprocessor", default=[])

args = parser.parse_args()

serial_info = generate(args.binary, args.define, args.include)

p = Popen(args.binary, stdin=PIPE, stdout=PIPE, close_fds=True)
engine = Engine(input=p.stdout, output=p.stdin, serial_info=serial_info, macro_hooks=[Exit, Unit])

assert engine.init_marker.file.endswith('unit.c')
assert engine.run() == 0