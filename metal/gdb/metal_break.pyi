import traceback
from abc import abstractmethod
from inspect import signature

import typing

import gdb


class Breakpoint:
    @property
    def identifier(self) -> str: ...
    def __init__(self, identifier: str): ...

    @staticmethod
    def is_valid() -> bool: ...

    def delete(self) -> None: ...

    @abstractmethod
    def stop(self, gdb_breakpoint : gdb.Breakpoint): ...

MetalBreakpoint = Breakpoint

class MetalBreak(gdb.Breakpoint):
    breaks: typing.Dict[str, Breakpoint]

    def __init__(self): ...

    def stop(self) -> typing.Optional[bool]: ...

    def add_metal_breakpoint(self, bp: Breakpoint): ...
    def delete_metal_breakpoint(self, bp: Breakpoint): ...


metal_break: MetalBreak

