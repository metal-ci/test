import json
import os
import pcpp

from typing import List, Dict, Set, Tuple

from .elfreader import Marker
from .location import Location


class LexToken:
    value: str
    lineno: int
    type: str
    lexpos: int
    source: str

    def __init__(self, value: str, lineno: int, type: str, lexpos: int, source: str):
        self.value = value
        self.lineno = lineno
        self.type = type
        self.lexpos = lexpos
        self.source = source

    def to_dict(self):
        return {
            'value':  self.value,
            'lineno': self.lineno,
            'type' :  self.type,
            'lexpos': self.lexpos,
            'source': self.source
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data['value'],
            data['lineno'],
            data['type'],
            data['lexpos'],
            data['source']
        )


def can_ignore(token: LexToken) -> bool:
    return token.type in ['CPP_WS', 'CPP_COMMENT1', 'CPP_COMMENT2']


class MacroExpansion:
    def __init__(self, name: str, args: List[str], args_token: List[List[LexToken]], file: str, line: int):
        self.name = name
        self.args = args
        self.args_token = args_token
        self.file = file
        self.line = line

    def to_dict(self):
        return {
            'name': self.name,
            'file': self.file,
            'line': self.line,
            'args': self.args,
            'args_tokenized': [[tk.to_dict() for tk in l] for l in self.args_token]
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data['name'],
            data['args'],
            [[LexToken.from_dict(tk) for tk in l] for l in data['args_token']],
            data['file'],
            data['line'])


class Preprocessor(pcpp.Preprocessor):
    expanded_macros : List[MacroExpansion]

    def __init__(self, macros: Set[str]):
        super().__init__()

        self.__macros = macros
        self.expanded_macros = []

    def macro_expand_args(self, macro: pcpp.preprocessor.Macro, args: List[List[LexToken]]):
        if macro.name in self.__macros:
            line = self.linemacro
            self.expanded_macros.append(
                MacroExpansion(name=macro.name,
                               args_token=[[LexToken(tk.value, tk.lineno, tk.type, tk.lexpos, tk.source) for tk in arg] for arg in args],
                               args=[''.join(tk.value for tk in arg) for arg in args], file=self.source, line=line))

        return super().macro_expand_args(macro, args)


def preprocess_compile_unit(absolute_path: str,
                            markers: List[Marker], defines: List[str] = [], paths: List[str] = [],
                            macros: List[str] = None):

    if macros is None:
        from metal.serial import default_hooks
        macros = [hook.identifier for hook in default_hooks]

    macros.extend(['METAL_SERIAL_INIT', 'METAL_SERIAL_EXIT'])

    proc = Preprocessor(set(macros))
    for m in macros:
        proc.define(m + '(...)')
    for d in defines:
        proc.define(d)
    for p in paths:
        proc.add_path(p)

    proc.parse(open(absolute_path).read(), absolute_path)
    proc.write(open(os.devnull, 'w'))


    for marker in (marker for marker in markers if marker.file == absolute_path):
        exps = [expanded_macro for expanded_macro in proc.expanded_macros if expanded_macro.file == marker.file and expanded_macro.line == marker.line]

        if len(exps) == 0:
            raise Exception(" {}:({}) No registered macro found for code marker.".format(marker.file, marker.line))
        elif len(exps) > 1:
            raise Exception(" {}:({}) Multiple registered macro found for code marker.".format(marker.file, marker.line))

    return proc.expanded_macros
