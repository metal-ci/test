import traceback
from abc import abstractmethod
from inspect import signature

import gdb


class MetalBreak(gdb.Breakpoint):
    def __init__(self):
        self.breaks = {}
        gdb.Breakpoint.__init__(self, "metal_break")

    def stop(self):
        fr = gdb.selected_frame()
        try:
            args = [arg for arg in fr.block() if arg.is_argument]

            fr.older().select()
            metal_breakpoint = str(args[0].value(fr).string())

            if metal_breakpoint in self.breaks:
                try:
                    for bp in self.breaks[metal_breakpoint]:
                        if len(signature(bp.stop).parameters) == 0:
                            bp.stop()
                        else:
                            bp.stop(self)

                except Exception as e:
                    gdb.write("Error in metal breakpoint {}: {}\n{}".format(metal_breakpoint, e, traceback.format_exc()), gdb.STDERR)
            return False
        except gdb.error as e:
            gdb.write("Error in metal_break.py: {}".format(e), gdb.STDERR)
            traceback.print_exc()
            raise e
        finally:
            fr.select()

    def add_metal_breakpoint(self, bp):
        if bp.identifier not in self.breaks:
            self.breaks[bp.identifier] = [bp]
        else:
            self.breaks[bp.identifier].append(bp)

    def delete_metal_breakpoint(self, bp):
        self.breaks[bp.identifier].remove(bp)


metal_break = MetalBreak()


class Breakpoint:
    @property
    def identifier(self):
        return self.__identifier

    def __init__(self, identifier):
        self.__identifier = identifier
        metal_break.add_metal_breakpoint(self)

    @staticmethod
    def is_valid():
        return metal_break.is_valid()

    def delete(self):
        metal_break.delete_metal_breakpoint(self)

    @abstractmethod
    def stop(self, gdb_breakpoint):
        pass


# Disambiguation from gdb.Breakpoint
MetalBreakpoint = Breakpoint
