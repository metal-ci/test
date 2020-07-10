from metal.gdb.metal_break import Breakpoint

from metal.gdb.exitcode import ExitBreakpoint
from metal.gdb.timeout import Timeout
from metal.gdb.newlib import NewlibBreakpoints

exit_ = ExitBreakpoint()
exit_.connect_event()

timeout = Timeout()
timeout.connect_events()

newlib_breakpoints = NewlibBreakpoints()