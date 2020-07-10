import collections
import re

import typing


from subprocess import PIPE, Popen

from .elfreader import Marker
from .generate import SerialInfo
from .hooks import MacroHook, Exit, Init
from .location import Location
from .preprocessor import MacroExpansion
from .read_symbols import Symbol

from math import log


def bytes_needed(n: int ):
    if n == 0:
        return 1
    return int(log(n, 256)) + 1

class Engine:

    serial_info: SerialInfo
    init_marker: Marker
    version_string = '__metal_serial_version_1'

    endianness: str
    base_pointer: int

    macro_hooks : typing.List[typing.Type[MacroHook]]

    def __init__(self, serial_info: SerialInfo, input: typing.IO, output: typing.Optional[typing.IO] = None,
                 macro_hooks: typing.List[typing.Type[MacroHook]] = None):

        if macro_hooks is None:
            from metal.serial import default_hooks
            self.macro_hooks = default_hooks
        else:
            self.macro_hooks = macro_hooks

        try:
            next(h for h in self.macro_hooks if isinstance(h, Init))
        except StopIteration:
            self.macro_hooks.append(Init)

        try:
            next(h for h in self.macro_hooks if isinstance(h, Exit))
        except StopIteration:
            self.macro_hooks.append(Exit)


        self.input = input
        self.output = output
        self.serial_info = serial_info

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

        self.base_pointer = metal_serial_write - serial_info.metal_serial_write.address

        if self.base_pointer is None:
            raise Exception('Could not determine base pointer, aborting')

        self.init_marker = self.find_marker(self.read_location())

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
        p =  self.read_int()
        if p < self.base_pointer:
            raise Exception("The value read was {}, which doesn't seem to be a code location".format(p))
        return p - self.base_pointer

    def write_memory(self, input: bytes) -> int:
        self.write_int(len(input))
        self.output.write(input)
        self.output.flush()
        return self.read_int()

    def read_memory(self) -> bytes:
        sz = self.read_int()
        return self.input.read(sz)
    
    def find_symbol(self, addr: int) -> str:
        for name, address in self.symbols:
            if address == addr:
                return name

    def find_marker(self, addr: int) -> Marker:
        try:
            return next(marker for marker in self.serial_info.markers if marker.address == addr)
        except StopIteration:
            raise Exception("Can't determine location for 0x{:x}".format(addr))

    def find_macro_expansion(self, marker: Marker) -> MacroExpansion:
        try:
            return next(expansion for expansion in self.serial_info.expansions if marker.file == expansion.file and marker.line == expansion.line)
        except StopIteration:
            raise Exception("{}({}) Can't find macro expansion.".format(marker.file, marker.line))

    def run(self) -> int:
        hooks = [Hook() for Hook in self.macro_hooks]
        exit_code_hook = next(hook for hook in hooks if isinstance(hook, Exit))

        while exit_code_hook.running:
            next_marker = self.find_marker(self.read_location())
            macro_expansion = self.find_macro_expansion(next_marker)
            try:
                hook = next((hook for hook in hooks if hook.identifier == macro_expansion.name))
                hook.invoke(self, macro_expansion)
            except StopIteration:
                raise Exception("Cannot find hook for macro '{}'".format(macro_expansion.name))

        for hook in hooks:
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



