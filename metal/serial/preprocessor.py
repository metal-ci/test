import json
import os
import pcpp

from typing import List, Dict, Set
from pycparser.ply import lex
from .location import Location

from pcpp.preprocessor import tokens as LexTokenTypes


class LexToken(lex.LexToken):
    value: str
    lineno: int
    type: str
    lexpos: int


def can_ignore(token: LexToken) -> bool:
    return token.type in ['CPP_WS', 'CPP_COMMENT1', 'CPP_COMMENT2']


class MacroExpansion:
    def __init__(self, name: str, args: List[str], args_token: List[List[LexToken]]):
        self.name = name
        self.args = args
        self.args_tokenized = args_token

class Preprocessor(pcpp.Preprocessor):
    expanded_macros : Dict[int, MacroExpansion]

    def __init__(self, macros: Set[str]):
        super().__init__()

        self.__macros = macros
        self.expanded_macros = {}

    def macro_expand_args(self, macro: pcpp.preprocessor.Macro, args: List[List[LexToken]]):
        if macro.name in self.__macros:
            line = self.linemacro
            # check if duplicate
            if line in self.expanded_macros:
                raise Exception('{}:{}: Two known macros defined.'.format(self.source, self.linemacro))

            self.expanded_macros[line] = MacroExpansion(name=macro.name, args_token=args, args=[''.join(tk.value for tk in arg) for arg in args])

        return super().macro_expand_args(macro, args)


class PreprocessedSource():
    paths: List[str]
    expansions: Dict[str, Dict[int, MacroExpansion]]
    macros: Set[str]

    def __init__(self, preloaded: Dict[str, Dict[int, MacroExpansion]] = {}, defines: List[str] = [], paths: List[str] = []):
        self.expansions = preloaded
        self.macros = set()
        self.defines = defines
        self.paths = paths

    def find_macro(self, location: Location) -> MacroExpansion:
        if location.file not in self.expansions:
            self.__process_file(location.file)

        return self.expansions[location.file][location.line]

    def __process_file(self, filename):
        proc = Preprocessor(self.macros)
        for m in self.macros:
            proc.define(m + '(...)')
        for d in self.defines:
            proc.define(d)
        for p in self.paths:
            proc.add_path(p)

        proc.parse(open(filename).read(), filename)
        proc.write(open(os.devnull, 'w'))

        self.expansions[filename] = proc.expanded_macros

    def add_macros(self, macros: List[str]):
        for macro in macros:
            self.macros.add(macro)
