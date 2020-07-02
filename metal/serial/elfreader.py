from os import path

from typing import Optional, List, Tuple

from elftools.dwarf.lineprogram import LineProgramEntry,  LineProgram
from elftools.elf.elffile import ELFFile
from elftools.elf.sections import SymbolTableSection

from itanium_demangler import parse as demangle


class Symbol:
    name: str
    demangled_name: Optional[str]
    address: int
    symbol_type: str

    def __init__(self, name: str, address: int, symbol_type: str, demangled_name: Optional[str] = None):
        self.name = name
        self.address = address
        self.symbol_type = symbol_type
        if demangled_name is None:
            self.demangled_name = demangle(name)
        else:
            self.demangled_name = demangled_name

    def __str__(self):
        if self.demangled_name and self.name == self.demangled_name:
            return '{:016x} {} {} {}'.format(self.address, self.symbol_type, self.name, self.demangled_name)
        else:
            return '{:016x} {} {}'.format(self.address, self.symbol_type, self.name)

    def __repr__(self):
        return self.__str__()

    def to_dict(self):
        return {
            'name' : self.name,
            'address' : self.address,
            'symbol_type' : self.symbol_type,
            'demangled_name': self.demangled_name
        }

    @classmethod
    def from_dict(cls, param):
        return cls(
            param['name'],
            param['address'],
            param['symbol_type'],
            param['demangled_name'])


class Marker(Symbol):
    def __init__(self, name: str, address: int, symbol_type: str, file: str, line: int, column: int):
        super().__init__(name, address, symbol_type)
        self.file = file
        self.line = line
        self.column = column

    def __str__(self):
        return '{:016x}, {} at {}:{}:{}'.format(self.address, self.name, self.file, self.line, self.column)

    def to_dict(self):
        return {
            'name' : self.name,
            'address' : self.address,
            'symbol_type' : self.symbol_type,
            'file' : self.file,
            'line' : self.line,
            'column' : self.column
        }

    @classmethod
    def from_dict(cls, param):
        return cls(
            param['name'],
            param['address'],
            param['symbol_type'],
            param['file'],
            param['line'],
            param['column'])



class CompileUnitInput:
    name: str
    compile_directory: str

    def __init__(self, name: str, compile_directory: str, files: List[str]):
        self.name = name
        self.compile_directory = compile_directory
        self.files = files

    @property
    def absolute_path(self):
        return self.name if path.isabs(self.name) else path.join(self.compile_directory, self.name)


class ELFReader:
    symbols: List[Symbol]
    markers: List[Marker]
    compile_units: List[CompileUnitInput]

    def __init__(self, binary: str):
        with open(binary, "rb") as b:
            elffile = ELFFile(b)

            #Symbol table
            for section in elffile.iter_sections():
                if isinstance(section, SymbolTableSection):
                    self.symbols = [Symbol(sym.name, sym['st_value'], sym['st_info']['type']) for sym in section.iter_symbols()
                                    if len(sym.name) > 0]

                    continue

            if not elffile.has_dwarf_info():
                raise Exception("This tool needs debug info.")

            dbg = elffile.get_dwarf_info()

            def file_entry_to_abs(file_entry, linep: LineProgram) -> str:
                di = file_entry.dir_index
                if di > 0:
                    return path.join(linep['include_directory'][di-1].decode(), file_entry.name.decode())
                else:
                    return path.join('.', file_entry.name.decode())

            cu_helper = [(cu, dbg.line_program_for_CU(cu)) for cu in dbg.iter_CUs()]

            self.compile_units = [
                CompileUnitInput(die.attributes['DW_AT_name'].value.decode(),
                                 die.attributes['DW_AT_comp_dir'].value.decode(),
                                 [file_entry_to_abs(fe, linep) for fe in linep['file_entry']])
                for cu, linep in cu_helper for die in cu.iter_DIEs() if die.tag == 'DW_TAG_compile_unit'
            ]

            # find compile units
            self.markers = []

            for msym in (sym for sym in self.symbols if sym.name.startswith('__metal_serial_')):
                try:
                    nx : Tuple[LineProgramEntry, LineProgram] = next((entry, linep) for (cu, linep) in cu_helper for entry in linep.get_entries()
                               if entry.state is not None and entry.state.address == msym.address)
                    (loc, linep) = nx

                    abs_file_entry = file_entry_to_abs(linep['file_entry'][loc.state.file - 1], linep)

                    # check if marker already exists -
                    for existing_marker in self.markers:
                        if loc.state.line == existing_marker.line and loc.state.column == existing_marker.column and existing_marker.file == abs_file_entry:
                            raise Exception("Duplicate code markers found at {}({})".format(existing_marker.file, existing_marker.line))

                    self.markers.append(Marker(
                        msym.name,
                        msym.address,
                        msym.symbol_type,
                        abs_file_entry,
                        loc.state.line,
                        loc.state.column
                    ))
                except StopIteration:
                    raise Exception('Could not find code location for {} at 0x{:x} - this is most likely due to missing debug symbols.'.format(msym.name, msym.address))

    def get_markers(self):
        return self.markers

    def get_functions(self):
        return (sym for sym in self.symbols if sym.symbol_type == "STT_FUNC")