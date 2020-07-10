import gdb
import metal


class ExitBreakpoint(gdb.Breakpoint, metal.gdb.Breakpoint):
    def __init__(self):
        gdb.Breakpoint.__init__(self, "_exit")
        metal.gdb.Breakpoint.__init__(self, 'exit')

        self.__exit_event = lambda event: self.handle_exit_event(event)

    def handle_exit_event(self, event):
        if hasattr(event, 'exit_code'):
            gdb.post_event(lambda : self.exit(event.exit_code))

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
            gdb.write("***metal-newlib*** Log: Invoking exit_ with {}\n".format(exit_code))
            gdb.execute("set confirm off")
            gdb.execute("quit {}".format(exit_code))
        except gdb.error as e:
            import traceback
            gdb.write("Error in metal-exitcode.py: {}\n\n{}".format(e, traceback.format_exc()))
            raise e

    def connect_event(self):
        gdb.events.exited.connect(self.__exit_event)

    def disconnect_event(self):
        gdb.events.exited.connect(self.__exit_event)

    def __enter__(self):
        self.connect_event()

    def __exit__(self):
        self.disconnect_event()
