import json
from typing import List

import argparse

from metal.serial.elfreader import ELFReader, Symbol, Marker
from metal.serial.preprocessor import MacroExpansion, preprocess_compile_unit


class SerialInfo:
    symbols: List[Symbol]
    metal_serial_write: Symbol
    expansions: List[MacroExpansion]
    markers: List[Marker]

    def __init__(self, symbols: List[Symbol], metal_serial_write: Symbol, expansions: List[MacroExpansion], markers: List[Marker]):
        self.metal_serial_write = metal_serial_write
        self.expansions = expansions
        self.markers = markers
        self.symbols = symbols

    def to_dict(self):
        return {
            'metal_serial_write': self.metal_serial_write.to_dict(),
            'expansions': [ex.to_dict() for ex in self.expansions],
            'markers': [marker.to_dict() for marker in self.markers],
            'symbols': [symbol.to_dict() for symbol in self.symbols],
        }

    @classmethod
    def from_dict(cls, data):
        return cls([Symbol.from_dict(sym) for sym in data['symbols']],
                    Symbol.from_dict(data['metal_serial_write']), expansions=[MacroExpansion.from_dict(expansion) for expansion in data['expansions']],
                    markers=[Marker.from_dict(marker) for marker in data['markers']])


def generate(binary: str, defines: List[str] = [], paths: List[str] = [], macros: List[str] = None) -> SerialInfo:

    if macros is None:
        from metal.serial import default_hooks
        macros = [hook.identifier for hook in default_hooks]

    elf_reader = ELFReader(binary)

    expansions : List[MacroExpansion] = []
    for cu in elf_reader.compile_units:
        expansions = expansions + preprocess_compile_unit(cu.absolute_path, paths=paths, macros=macros, defines=defines, markers=elf_reader.get_markers())

    return SerialInfo(elf_reader.symbols, next(sym for sym in elf_reader.symbols if sym.name == 'metal_serial_write'),expansions, elf_reader.get_markers())


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('binary',                     help='The binary that runs on target')
    parser.add_argument('-S', '--source-dir',  required=True, help='The root of the source directory')
    parser.add_argument('-I', '--include', nargs='+', help="Include folders for the preprocessor", default=[])
    parser.add_argument('-D', '--define',  nargs='+', help="Defines for the preprocessor", default=[])
    parser.add_argument('-O', '--output',             help='The file to write the generated data to')

    args = parser.parse_args()

    res = json.dumps(generate(args.binary, args.define, args.include).to_dict())

    if args.output:
        with open(args.output, "w") as f:
            f.write(res)
    else:
        print(res)


if __name__ == '__main__':
    main()
