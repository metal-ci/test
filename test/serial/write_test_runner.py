import re
import sys
import argparse
import pcpp

from metal.serial import Engine, read_symbols
from subprocess import PIPE, Popen
from metal.serial.preprocessor import PreprocessedSource

parser = argparse.ArgumentParser()

parser.add_argument('binary',           help='The binary that runs on target')
parser.add_argument('-S', '--source-dir',  required=True, help='The root of the source directory')
parser.add_argument('-D', '--bin-dir',     required=True, help='The binary directory')
parser.add_argument('-A', '--addr2line',   default='addr2line', help='The addr2line command for evaluating the binary')
parser.add_argument('-N', '--nm',          default='nm', help='The nm command for evaluating the binary')

args = parser.parse_args()

symbols = read_symbols(nm= args.nm, binary=args.binary)

p = Popen(args.binary, stdin=PIPE, stdout=PIPE, stderr=sys.stdout.buffer, close_fds=True)

preproc = PreprocessedSource()
engine = Engine(binary=args.binary, input=p.stdout, output=p.stdin, symbols=symbols, addr2line=args.addr2line, preprocessed_source=preproc)


assert engine.init_location.file.endswith('write.c')
assert engine.init_location.line == 25

engine.write_byte(b'0')
assert engine.read_byte() == b'9'

engine.write_int(22)
assert engine.read_int() == 44

assert engine.write_string("str") == 3
assert engine.read_string() == "tr"

engine.write_int(11)
assert engine.read_int() == 33

assert engine.write_string("overflow") == 6
assert engine.read_string() == "erfl"

engine.write_int(4)
assert engine.read_int() == 16

assert engine.write_memory(b'\x00\x01\x02\x03\x04') == 4
assert engine.read_memory() == b'\x03\x02\x01\x00'

assert engine.write_memory(b'1234567890') == 4
assert engine.read_memory() == b'1234'

assert engine.run([]) == 123


