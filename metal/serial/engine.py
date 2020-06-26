import collections
import re

import typing


from subprocess import PIPE, Popen

from pycparser.ply.lex import LexToken

from .location import Location
from .preprocessor import PreprocessedSource
from .read_symbols import Symbol

from math import log


def bytes_needed(n: int ):
    if n == 0:
        return 1
    return int(log(n, 256)) + 1


class MacroHook:
    identifier: str

    def invoke(self, engine: 'Engine', args: typing.List[str], args_tokenized: typing.List[typing.List[LexToken]]):
        raise NotImplementedError

    def exit(self, exit_code: int):
        pass


class DefaultExit(MacroHook):
    identifier = 'METAL_SERIAL_EXIT'
    exit_code: typing.Optional[int]

    def invoke(self, engine: 'Engine', args: typing.List[str], args_tokenized: typing.List[typing.List[LexToken]]):
        self.exit_code = engine.read_int()

    def __init__(self):
        super().__init__()

        self.exit_code = None

    @property
    def running(self):
        return self.exit_code is None


class Engine:

    init_location: Location
    version_string = '__metal_serial_version_1'

    endianness: str
    base_pointer: int

    def __init__(self, binary: str, addr2line: str, symbols: typing.List[Symbol],
                 preprocessed_source: PreprocessedSource,
                 input: typing.IO, output: typing.Optional[typing.IO] = None):
        self.input = input
        self.output = output
        self.symbols = symbols
        self.preprocessed_source = preprocessed_source

        # Initialize the connection
        target_version = self.read_string()
        assert target_version == Engine.version_string

        self.int_length = int.from_bytes(self.read_byte(), 'big')
        endian_checker = input.read(self.int_length)

        if self.int_length == 1:
            if endian_checker == b'\x43':
                self.endianness = 'little'
            elif endian_checker == b'\x6C':
                self.endianness = 'big'
        elif self.int_length == 2:
            if endian_checker == b'\x43\x6C':
                self.endianness = 'little'
            elif endian_checker == b'\x6C\x43':
                self.endianness = 'big'
        elif self.int_length == 4:
            if endian_checker ==  b'\x43\x6C\x00\x00':
                self.endianness = 'little'
            elif endian_checker == b'\x00\x00\x6C\x43':
                self.endianness = 'big'
        elif self.int_length == 8:
            if endian_checker == b'\x43\x6C\x00\x00\x00\x00\x00\x00':
                self.endianness = 'little'
            elif endian_checker == b'\x00\x00\x00\x00\x00\x00\x6C\x43':
                self.endianness = 'big'

        if self.endianness is None:
            raise Exception('Invalid endianness checker {}'.format(endian_checker))

        metal_serial_write = self.read_int()

        for sym in symbols:
            if sym.name == 'metal_serial_write':
                self.base_pointer = metal_serial_write - sym.address

        if self.base_pointer is None:
            raise Exception('Could not determine base pointer, aborting')

        self.addr2line = Popen([addr2line, '--exe', binary], stdout=PIPE,stdin=PIPE, )
        self.init_location = self.find_location(self.read_location())

    def read_byte(self) -> bytes :
        return self.input.read(1)

    def write_byte(self, param: bytes):
        self.output.write(param[:1])
        self.output.flush()

    def read_string(self) -> str:
        chars = bytearray()
        while True:
            c = self.read_byte()
            if c == b'\x00':
                return chars.decode()
            chars.extend(c)

    def write_string(self, param: str) -> int:
        self.output.write(param.encode() + b'\x00')
        self.output.flush()
        return self.read_int()

    def read_int(self) -> int:
        sz = self.input.read(1)
        assert 0 < int.from_bytes(sz, self.endianness) < 16
        value = self.input.read(int.from_bytes(sz, self.endianness))
        return int.from_bytes(value, byteorder=self.endianness)

    def write_int(self, param: int):
        as_bytes = param.to_bytes(bytes_needed(param), self.endianness)
        self.output.write(len(as_bytes).to_bytes(1, self.endianness))
        self.output.write(as_bytes)
        self.output.flush()

    def read_location(self) -> int:
        return self.read_int() - self.base_pointer

    def write_memory(self, input: bytes) -> int:
        self.write_int(len(input))
        self.output.write(input)
        self.output.flush()
        return self.read_int()


    def read_memory(self) -> bytes:
        sz = self.read_int()
        return self.input.read(sz)

    def find_symbol(self, addr: int)-> str:
        for name, address in self.symbols:
            if address == addr:
                return name

    def find_location(self, addr: int) -> Location:
        msg = '0x{:x}\n'.format(addr).encode()
        self.addr2line.stdin.write(msg)
        self.addr2line.stdin.flush()
        res = self.addr2line.stdout.readline().decode().strip()
        if res == '??:0':
            raise Exception("Can't determine location for 0x{:x}".format(addr))

        mt = re.fullmatch('^((?:\w:)?[^:]+):(\d+)(?:\s+\(discriminator \d+\))?\s*$', res)
        if not mt:
            raise Exception("Error reading from addr2line {}".format(res))

        return Location(mt[1], int(mt[2]))

    def run(self, macro_hooks: typing.List[MacroHook] = []) -> int:
        duplicates = [hookname for hookname, count in collections.Counter([hook.identifier for hook in macro_hooks]).items() if count > 1]
        if len(duplicates) > 0:
            raise Exception('Duplicate Macro identifiers ' + ','.join(duplicates))

        exit_code_hook = DefaultExit()
        macro_hooks.append(exit_code_hook)
        self.preprocessed_source.add_macros([hook.identifier for hook in macro_hooks])

        while exit_code_hook.running:
            next_location = self.find_location(self.read_location())
            mc = self.preprocessed_source.find_macro(next_location)
            next((hook for hook in macro_hooks if hook.identifier == mc.name)).invoke(self, mc.args, mc.args_tokenized)

        for hook in macro_hooks:
            hook.exit(exit_code_hook.exit_code)

        return exit_code_hook.exit_code

    def read_with_type(self):
        type_ = self.read_byte()
        if type_ == b'b':
            return self.read_byte()
        if type_ == b'i':
            return self.read_int()
        if type_ == b's':
            return self.read_string()
        if type_ == b'x':
            return self.read_memory()
        if type_ == b'p':
            return self.read_int()
        if type_ == b'l':
            return self.read_location()

        raise Exception('Unknown type "{}" sent'.format(type_))


