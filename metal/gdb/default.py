from metal.gdb.argv import ArgvBreakpoint
from metal.gdb.metal_break import Breakpoint

from metal.gdb.exitcode import ExitBreakpoint
from metal.gdb.timeout import Timeout
from metal.gdb.newlib import NewlibBreakpoints

exit_ = ExitBreakpoint()
exit_.connect_event()

timeout = Timeout()
timeout.connect_events()

newlib_breakpoints = NewlibBreakpoints()
argv = ArgvBreakpoint()

from metal.gdb.unit import UnitBreakpoint
from metal.unit import Reporter

rep = Reporter()
unit = UnitBreakpoint(rep)