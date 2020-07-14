import sys
import typing

from metal.serial import Engine
from metal.serial.hooks import MacroHook
from metal.serial.preprocessor import MacroExpansion


class Argv(MacroHook):
    identifier = 'METAL_SERIAL_INIT_ARGV'

    def invoke(self, engine: Engine, macro_expansion: MacroExpansion):

        engine.write_int(len(self.argv))
        data = b'\0'.join(arg.encode() for arg in self.argv) + b'\0'
        res = engine.write_memory(data)
        if res != len(data):
            print("***metal.serial***: Couldn't write all of argv, buffer size was {}".format(res), file=sys.stderr)

    def __init__(self, argv: typing.List[str]):
        self.argv = argv
        super().__init__()


def build_argv_hook(argv: typing.List[str]):
    return lambda : Argv(argv)