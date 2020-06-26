import re
import sys
import argparse
import pcpp
from elftools.elf.descriptions import describe_reloc_type
from elftools.elf.relocation import RelocationSection
from elftools.elf.sections import SymbolTableSection

from metal.serial import Engine, read_symbols
from subprocess import PIPE, Popen, check_output

from metal.serial.elfreader import ELFReader
from metal.serial.preprocessor import PreprocessedSource



parser = argparse.ArgumentParser()

parser.add_argument('binary',           help='The binary that runs on target')
parser.add_argument('-S', '--source-dir',  required=True, help='The root of the source directory')
parser.add_argument('-D', '--bin-dir',     required=True, help='The binary directory')
parser.add_argument('-O', '--objdump',   default='addr2line', help='The addr2line command for evaluating the binary')
parser.add_argument('-N', '--nm',          default='nm', help='The nm command for evaluating the binary')
parser.add_argument('-I', '--include', nargs='+', help="Include folders", default=[])

args = parser.parse_args()

elfReader = ELFReader(args.binary)

symbols = read_symbols(nm=args.nm, binary=args.binary)

p = Popen(args.binary, stdin=PIPE, stdout=PIPE, close_fds=True)

preproc = PreprocessedSource(paths=args.include)

engine = Engine(binary=args.binary, input=p.stdout, output=p.stdin, symbols=symbols, addr2line=args.addr2line, preprocessed_source=preproc)

assert engine.init_location.file.endswith('read.c')
assert engine.init_location.line == 22

assert engine.read_byte() == b'a'
assert engine.read_int() == 42
assert engine.read_string() == "test-string"

main_ptr = engine.read_int() - engine.base_pointer
assert [sym.address for sym in symbols if sym.name == 'main'][0] == main_ptr

assert int.from_bytes(engine.read_memory(), engine.endianness) == 42
assert engine.read_int() == 1234

assert engine.run([]) == 42

