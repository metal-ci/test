import typing
import re

from metal.serial import MacroHook, Engine
from metal.serial.preprocessor import MacroExpansion
from metal.unit import Reporter

level_t = ["cancel", "info", "enter", "exit", "assert", "expect"]
type_t = ["plain", "critical", "critical_section", "loop", "ranged", "message", "call", "log", "checkpoint", "equal", "not_equal", "predicate", "close", "close_relative", "ge", "le", "greater", "lesser", "report" ];




class Unit(MacroHook):
    identifier = 'METAL_TEST_REPORT_IMPL'
    exit_code: typing.Optional[int]

    def invoke(self, engine: Engine, macro_expansion: MacroExpansion):
        file = macro_expansion.file
        line = macro_expansion.line
        
        type_and_level = engine.read_byte()
        args = macro_expansion.args[3:]

        level = level_t[(type_and_level[0] & 0b11100000) >> 5]
        type_ = type_t[type_and_level[0] & 0b11111]

        cond_or_length = engine.read_int()
        condition = bool(cond_or_length)
        func = getattr(self.reporter, type_)

        if type_ == "checkpoint":
            func(file, line)
        elif type_ == "log":
            func(file, line, args[0])
        elif type_ in ["message", "plain"]:
            func(file, line, level, condition, args[0])
        elif type_ in ["equal",  "not_equal",  "ge",  "le",  "greater",  "lesser"]:
            func(file, line, level, condition, args[0], args[1])
        elif type_ in ["close", "close_relative"]:
            func(file, line, level, condition, args[0], args[1], args[2])
        elif type_ in ["close", "close_relative"]:
            func(file, line, level, condition, args[0], args[1], args[2])
        elif type_ == "report":
            func(file, line, condition)
        elif type_ == "critical":
            func(file, line, level)
        elif type_  == "call":
            name = args[1][3:-8] if args[1] else args[0]
            func(file, line, level, condition, name)
        elif type_ == 'loop':
            func(file, line, level)
        elif type_ == 'ranged':
            func(file, line, level, cond_or_length, args)
        elif type_ == 'predicate':
            args_a = [arg.strip() for arg in str(args[1][2:-2]).split(',')] if args else None
            func(file, line, level, cond_or_length, args[0], args_a)
        else:
            raise Exception("Unknown check type {}".format(type_))
         
    def __init__(self, reporter=None):
        super().__init__()
        if reporter:
            self.reporter = reporter
        else:
            self.reporter = Reporter()

