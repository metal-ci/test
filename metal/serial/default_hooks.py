import typing as __typing

from metal.serial import MacroHook, Init, DefaultExit

from metal.serial import newlib
default_hooks: __typing.List[__typing.Type[MacroHook]] = [Init, DefaultExit, newlib.Syscall]