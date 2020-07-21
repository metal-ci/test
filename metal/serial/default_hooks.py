import typing as __typing

from metal.serial import MacroHook, Init, Exit
from metal.serial import newlib, unit


default_hooks: __typing.List[__typing.Type[MacroHook]] = [newlib.Syscall, unit.Unit]