import argparse
import errno
import os

from metal.serial import Engine, Exit, MacroHook
from subprocess import PIPE, Popen

from metal.serial.argv import build_argv_hook
from metal.serial.generate import generate

from metal.serial.newlib import build_newlib_hook
from metal.serial.preprocessor import MacroExpansion

parser = argparse.ArgumentParser()

parser.add_argument('binary',           help='The binary that runs on target')
parser.add_argument('-S', '--source-dir',  required=True, help='The root of the source directory')
parser.add_argument('-I', '--include', nargs='+', help="Include folders for the preprocessor", default=[])
parser.add_argument('-D', '--define', nargs='+', help="Defines for the preprocessor", default=[])

args = parser.parse_args()

serial_info = generate(args.binary, args.define, args.include, ['METAL_SERIAL_INIT_ARGV', 'METAL_SERIAL_TEST'])
argv_ = []

class ArgvTest(MacroHook):
    identifier = 'METAL_SERIAL_TEST'

    def invoke(self, engine: Engine, macro_expansion: MacroExpansion):
        l = engine.read_int()
        global argv_
        argv_ = [engine.read_string() for i in range(l)]

    def __init__(self):
        global argv_
        argv_ = []
        super().__init__()


def test_args(argv, argv_ex=None):
    if argv_ex is None:
        argv_ex = argv

    p = Popen(args.binary, stdin=PIPE, stdout=PIPE, close_fds=True)
    engine = Engine(input=p.stdout, output=p.stdin, serial_info=serial_info, macro_hooks=[Exit, build_argv_hook(argv), ArgvTest])

    print('testing with ', argv)
    assert engine.init_marker.file.endswith('argv.c')
    assert engine.run() == 0

    print('received ', argv_)
    print('expected ', argv_ex)
    assert argv_ == argv_ex


test_args(['foo', 'bar'])
test_args(['overflow', 'arguments'], ['overflow'])
test_args(['one overflowing argument '], [])
test_args(['foo', 'bar', 'foobar'], ['foo', 'bar'])