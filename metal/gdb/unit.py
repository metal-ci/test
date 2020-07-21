import re
import sys
import json
import traceback
import sys
import gdb
import metal

str = str
if sys.version_info[0] < 3:
    str = unicode


class DisableExitCode(gdb.Parameter):
    def __init__(self):
        super(DisableExitCode, self).__init__("metal-unit-exit-code",
                                              gdb.COMMAND_DATA,
                                              gdb.PARAM_BOOLEAN)
        self.value = True

    set_doc = '''Set exit-code propagation.'''
    show_doc = '''This parameter enables assignment of the exit-code on test exit.'''


class SelectHrfSink(gdb.Parameter):
    def __init__(self, reporter):
        super(SelectHrfSink, self).__init__("metal-unit-hrf-sink",
                                             gdb.COMMAND_DATA,
                                             gdb.PARAM_OPTIONAL_FILENAME)
        self.value = "stdout"
        self.sink = sys.stdout
        self.reporter = reporter

    def get_set_string(self):
        if self.value is None:
            self.sink = None
        elif self.value == 'stdout':
            self.sink = sys.stdout
        elif self.value == 'stderr':
            self.sink = sys.stderr
        else:
            self.sink = open(self.value, 'w')

        self.reporter.hrf_sink = self.sink
        return self.value

    set_doc = '''Set output file.'''
    show_doc = '''This sets the test data output sink.'''


class SelectJsonSink(gdb.Parameter):
    def __init__(self, reporter):
        super(SelectJsonSink, self).__init__("metal-unit-json-sink",
                                             gdb.COMMAND_DATA,
                                             gdb.PARAM_OPTIONAL_FILENAME)
        self.value = None
        self.sink = None
        self.reporter = reporter

    def get_set_string(self):
        if self.value is None:
            self.sink = None
        elif self.value == 'stdout':
            self.sink = sys.stdout
        elif self.value == 'stderr':
            self.sink = sys.stderr
        else:
            self.sink = open(self.value, 'w')
        print(self.value, self.sink)
        self.reporter.json_sink = self.sink
        return self.value

    set_doc = '''Set output file.'''
    show_doc = '''This sets the test data output sink.'''


class PrintLevel(gdb.Parameter):
    def __init__(self):
        super(PrintLevel, self).__init__("metal-unit-print-level",
                                         gdb.COMMAND_DATA,
                                         gdb.PARAM_ENUM, ["all", "warning", "error"])
        self.value = "all"

    set_doc = '''Set the level for logging.'''
    show_doc = '''This sets the level for notifications to be printed.'''

printLevel = PrintLevel()


class FrameSelector:
    def __init__(self, frame, idx = 1):
        self.frame = frame
        self.index = idx

    def __enter__(self):
        fr = self.frame
        for i in range(0, self.index):
            fr = fr.older()
        fr.select()
        return self

    def __exit__(self, x, y, z):
        self.frame.select()


def print_from_frame(frame, name, frame_nr=1):
    with FrameSelector(frame, frame_nr):
        val = gdb.parse_and_eval(name)
        str(val)


class FrameHelper:
    def __init__(self, fr):
        if fr is None:
            fr = gdb.selected_frame()

        self.frame = fr
        # type, lvl, cond_or_len, const char* file, int line, const char *arg0, const char *arg1, const char *arg2, const char *arg3
        self.args = [arg for arg in fr.block() if arg.is_argument]

        # plain critical critical_section for ranged_enter ranged_exit ranged message call_enter call_exit log checkpoint equal not_equal predicate close close_relative ge le greater lesser
        self.type = str(self.args[0].value(fr))[len('metal_unit_type_'):]

        # cancel info assert expect
        self.level = str(self.args[1].value(fr))[len('metal_unit_level_'):]

        # 1 == true
        self.cond_or_length = int(str(self.args[2].value(fr)))
        self.failed = self.cond_or_length == 0
        self.file = str(self.args[3].value(fr).string())
        self.line = int(str(self.args[4].value(fr)))


    def get_arg(self, idx):
        val = self.args[5 + idx].value(self.frame)
        if val != 0:
            return str(self.args[5 + idx].value(self.frame).string())

    def print_from_parent_frame(self, name, frame_nr=1):
        with FrameSelector(self.frame, frame_nr):
            val = gdb.parse_and_eval(name)
            return val

    def print_arg(self, idx):
        arg = self.get_arg(idx)
        if arg is not None:
            return self.print_from_parent_frame(arg)

    def str_arg(self, idx):
        arg = self.get_arg(idx)
        if arg is not None:
            return str(self.print_from_parent_frame(arg))

    @property
    def length(self): return int(self.cond_or_length)

    @property
    def condition(self): return bool(self.cond_or_length)


class UnitBreakpoint(metal.gdb.Breakpoint):
    def __init__(self, reporter):
        metal.gdb.Breakpoint.__init__(self, "metal.unit")

        self.selectJsonSink = SelectJsonSink(reporter)
        self.SelectHrfSink = SelectHrfSink(reporter)
        self.disableExitCode = DisableExitCode()
        self.reporter = reporter

    def stop(self, gdb_breakpoint):
        try:
            fr = FrameHelper(gdb.selected_frame())

            func = getattr(self.reporter, fr.type)
            if fr.type == "checkpoint":
                func(fr.file, fr. line)
            elif fr.type == "log":
                func(fr.file, fr. line, fr.str_arg(0))
            elif fr.type in ["message", "plain"]:
                func(fr.file, fr. line, fr.level, fr.condition, fr.str_arg(0))
            elif fr.type in ["equal",  "not_equal",  "ge",  "le",  "greater",  "lesser"]:
                func(fr.file, fr. line, fr.level, fr.condition, fr.get_arg(0), fr.get_arg(1), fr.str_arg(0), fr.str_arg(1))
            elif fr.type in ["close", "close_relative"]:
                func(fr.file, fr. line, fr.level, fr.condition, fr.get_arg(0), fr.get_arg(1), fr.get_arg(2), fr.str_arg(0), fr.str_arg(1), fr.str_arg(2))
            elif fr.type in ["close", "close_relative"]:
                func(fr.file, fr. line, fr.level, fr.condition, fr.get_arg(0), fr.get_arg(1), fr.get_arg(2), fr.str_arg(0), fr.str_arg(1), fr.str_arg(2))
            elif fr.type == "report":
                func(fr.file, fr. line, fr.condition)
            elif fr.type == "critical":
                func(fr.file, fr. line, fr.level)
            elif fr.type  == "call":
                func(fr.file, fr. line, fr.level, fr.condition, fr.str_arg(0))
            elif fr.type == 'loop':
                func(fr.file, fr. line, fr.level)
            elif fr.type == 'ranged':
                func(fr.file, fr. line, fr.level, fr.cond_or_length, [fr.get_arg(i) for i in range(4)], [fr.str_arg(i) for i in range(4)])
            elif fr.type == 'predicate':
                args = fr.print_arg(1)
                args_a = str(args).split(',') if args else None
                args_v = [str(fr.print_from_parent_frame(arg)) for arg in args_a] if args_a else None
                func(fr.file, fr. line, fr.level, fr.cond_or_length, fr.get_arg(0), args_a, fr.str_arg(0), args_v)
            else:
                raise Exception("Unknown check type {}".format(fr.type))

            return False
        except Exception as e:
            gdb.write("Error in metal-unit.py: {}".format(e), gdb.STDERR)
            traceback.print_exc()
            raise e

