import traceback
import gdb
import metal


class ExitBreakpoint(gdb.Breakpoint, metal.gdb.Breakpoint):
    def __init__(self):
        gdb.Breakpoint.__init__(self, "_exit")
        metal.gdb.Breakpoint.__init__(self, 'exit')

    def stop(self):
        frame = gdb.selected_frame()
        args = [arg for arg in frame.block() if arg.is_argument]

        exit_code = None
        for arg in args:
            exit_code = str(arg.value(frame))
            break

        gdb.post_event(lambda: self.exit(exit_code))

        return True

    def exit(self, exit_code):
        try:
            gdb.write("***metal-newlib*** Log: Invoking _exit with {}\n".format(exit_code))
            gdb.execute("set confirm off")
            gdb.execute("quit {}".format(exit_code))
        except gdb.error as e:
            gdb.write("Error in metal-exitcode.py: {}".format(e))
            traceback.print_exc()
            raise e


_exit = ExitBreakpoint()


def exit_event(event):
    if hasattr(event, 'exit_code'):
        gdb.post_event(lambda : _exit.exit(event.exit_code))


gdb.events.exited.connect(exit_event)
