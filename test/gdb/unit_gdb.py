from metal.gdb.unit import UnitBreakpoint

from metal.unit import Reporter


class TestReporter(Reporter):
    def __init__(self):
        super().__init__()

    def report(self, file, line, condition):
        super().report(file, line, condition)
        assert self.current_scope.executed == 76
        assert self.current_scope.warnings == 13
        assert self.current_scope.errors == 16

rep = TestReporter()
unit = UnitBreakpoint(rep)
