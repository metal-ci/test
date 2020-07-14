import errno
import os
import sys
import typing
from metal.cpputest import TestResult, UtestShell, TestFailure, CppUTestOutput

from metal.newlib import Flags, map_errno, map_open_flags, map_file_mode
from metal.serial import Engine
from metal.serial.hooks import MacroHook
from metal.serial.preprocessor import MacroExpansion


def read_test_result(engine: Engine) -> TestResult:
    res = TestResult()

    res.testCount = engine.read_int()
    res.runCount = engine.read_int()
    res.checkCount = engine.read_int()
    res.filteredOutCount = engine.read_int()
    res.ignoredCount = engine.read_int()
    res.failureCount = engine.read_int()
    res.totalExecutionTime = engine.read_int()
    res.currentTestTotalExecutionTime = engine.read_int()
    res.currentGroupTotalExecutionTime = engine.read_int()

    return res


def read_test_shell(engine: Engine) -> UtestShell:
    res = UtestShell()

    res.name = engine.read_string()
    res.group = engine.read_string()
    res.formattedName = engine.read_string()
    res.file = engine.read_string()
    res.lineNumber = engine.read_int()

    return res


def read_test_failure(engine: Engine) -> TestFailure:
    res = TestFailure()

    res.fileName = engine.read_string()
    res.testName = engine.read_string()
    res.testNameOnly = engine.read_string()
    res.failureLineNumber = engine.read_int()
    res.message = engine.read_string()
    res.testFileName = engine.read_string()
    res.testLineNumber = engine.read_int()
    res.isOutsideTestFile = engine.read_byte()[0] != 0
    res.isInHelperFunction = engine.read_byte()[0] != 0

    return res

class CppUTest(MacroHook):
    identifier = 'METAL_SERIAL_CPPUTEST'

    def invoke(self, engine: Engine,  macro_expansion: MacroExpansion):

        vargs = macro_expansion.args[0].split(',')
        func = vargs[0]
        spec = vargs[1] if len(vargs) > 1 else None

        try:
            if spec is None:
                self.func_map[func](engine)
            else:
                self.func_map[func](engine, spec.strip())
        except AttributeError:
            raise Exception("Function {} not found for cpputest".format(func))
        except OSError as e:
            print('OSerror', e)

    def __init__(self, output: CppUTestOutput):
        self.output = output
        super().__init__()

        self.func_map = {
            "printTestsStarted" : lambda e: output.print_tests_started(),
            "printTestsEnded"   : lambda e: output.print_tests_ended(read_test_result(e)),
            "printCurrentTestStarted" : lambda e: output.print_current_test_started(read_test_shell(e)),
            "printCurrentTestEnded"   : lambda e: output.print_current_test_ended(read_test_result(e)),
            "printCurrentGroupStarted": lambda e: output.print_current_group_started(read_test_shell(e)),
            "printCurrentGroupEnded"  : lambda e: output.print_current_group_ended(read_test_result(e)),
            "verbose" : lambda e: output.verbose(e.read_int()),
            "color" : lambda e: output.color(),
            "printBuffer" : lambda e: output.print_buffer(e.read_string()),
            "print": lambda e, t:
            output.print(
                {'str': lambda e_: e_.read_string(),
                 'int': lambda e_: e_.read_int(),
                 "double": lambda e_: float(e_.read_string())
                 }[t](e)),
            "printFailure": lambda e: output.print_failure(read_test_failure(e)),
            "printTestRun": lambda e: output.print_test_run(e.read_int(), e.read_int()),
            "setProgressIndicator": lambda e: output.set_progress_indicator(e.read_string()),
            "printVeryVerbose": lambda e: output.print_very_verbose(e.read_string()),
            "flush": lambda e: output.flush()
        }




