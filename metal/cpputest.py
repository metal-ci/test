level_quiet: int = 0
level_verbose: int = 1
level_veryVerbose:int  = 2

class TestResult:
    pass

class UtestShell:
    pass

class TestFailure:
    pass

class CppUTestOutput:
    def print_tests_started(self): pass
    def print_tests_ended(self, result): pass
    def print_current_test_started(self, test_shell): pass
    def print_current_test_ended(self, test_result): pass
    def print_current_group_started(self, test_shell): pass
    def print_current_group_ended(self, test_result): pass
    def verbose(self, level: int): pass
    def color(self): pass
    def print_buffer(self, buffer: str): pass

    def print(self, data): pass

    def print_double(self, d): pass
    def print_failure(self, failure): pass
    def print_test_run(self, number, total): pass
    def set_progress_indicator(self, indicator): pass

    def print_very_verbose(self, msg): pass

    def flush(self): pass

