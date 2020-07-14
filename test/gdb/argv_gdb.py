from metal.gdb import ArgvBreakpoint
from metal.gdb.exitcode import ExitBreakpoint
from metal.gdb.timeout import Timeout


exit_ = ExitBreakpoint()
exit_.connect_event()

timeout = Timeout()
timeout.connect_events()

argv = ArgvBreakpoint()