
from subprocess import check_output
from typing import List, Optional


class Symbol:
    name: str
    demangled_name: Optional[str]
    address: int
    symbol_type: str

    def __init__(self, name: str, address: int, symbol_type: str, demangled_name: Optional[str] = None):
        self.name = name
        self.address = address
        self.symbol_type = symbol_type
        self.demangled_name = demangled_name

    def __str__(self):
        if self.demangled_name and self.name == self.demangled_name:
            return '{:016x} {} {} {}'.format(self.address, self.symbol_type, self.name, self.demangled_name)
        else:
            return '{:016x} {} {}'.format(self.address, self.symbol_type, self.name)


def read_symbols(nm: str, binary: str, demangle: bool = True) -> List[Symbol]:
    symbols = [Symbol(name, int(address, 16), type) for address, type, name in  (ln.split(" ") for ln in check_output([nm, binary]).decode().splitlines()) if type.lower() == "t" and not name.startswith('.')]

    if demangle:
        demangled = [Symbol(name, int(address, 16), type) for address, type, name in  (ln.split(" ", 2) for ln in check_output([nm, binary, '--demangle']).decode().splitlines()) if type.lower() == "t" and not name.startswith('.')]

        for sym in symbols:
            sym.demangled_name = next(dsym.name for dsym in demangled)

    return symbols
