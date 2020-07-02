import typing

from pycparser.ply.lex import LexToken


class MacroHook:
    identifier: str

    def invoke(self, engine: 'Engine', macro_expansion: 'MacroExpansion'):
        raise NotImplementedError

    def exit(self, exit_code: int):
        pass


class Init(MacroHook):
    identifier = 'METAL_SERIAL_INIT'

    def __init__(self):
        super().__init__()

    def invoke(self, engine: 'Engine', macro_expansion: 'MacroExpansion'):
        pass


class DefaultExit(MacroHook):
    identifier = 'METAL_SERIAL_EXIT'
    exit_code: typing.Optional[int]

    def invoke(self, engine: 'Engine',  macro_expansion: 'MacroExpansion'):
        self.exit_code = engine.read_int()

    def __init__(self):
        super().__init__()

        self.exit_code = None

    @property
    def running(self):
        return self.exit_code is None


default_hooks: typing.List[typing.Type[MacroHook]] = [Init, DefaultExit]

