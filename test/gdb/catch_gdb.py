from metal.gdb.unit import UnitBreakpoint

from metal.unit import Reporter


class TestReporter(Reporter):
    def __init__(self):
        super().__init__()

    def report(self, file, line, condition):
        super().report(file, line, condition)
        assert self.current_scope.executed == 23
        assert self.current_scope.warnings == 1
        assert self.current_scope.errors == 13

rep = TestReporter()
unit = UnitBreakpoint(rep)
