import typing


class TestResult:
    testCount: int
    runCount: int
    checkCount: int
    filteredOutCount: int
    ignoredCount: int
    failureCount: int
    totalExecutionTime: int
    currentTestTotalExecutionTime: int
    currentGroupTotalExecutionTime: int

class UtestShell:
    name: str
    group: str
    formattedName: str
    file: str
    lineNumber: int

class TestFailure:
    fileName: str
    testName: str
    testNameOnly: str

    failureLineNumber: int

    message: str
    testFileName: str

    testLineNumber: int

    isOutsideTestFile: bool
    isInHelperFunction: bool

level_quiet: int
level_verbose: int
level_veryVerbose:int

class CppUTestOutput:
    def print_tests_started(self): ...
    def print_tests_ended(self, result: TestResult): ...
    def print_current_test_started(self, test: UtestShell): ...
    def print_current_test_ended(self, res: TestResult): ...
    def print_current_group_started(self, test: UtestShell): ...
    def print_current_group_ended(self, res: TestResult): ...
    def verbose(self, level: int): ...
    def color(self): ...
    def print_buffer(self, buffer: str): ...

    def print(self, data: typing.Union[int, str, float]): ...

    def print_failure(self, failure: TestFailure): ...
    def print_test_run(self, number: int, total: int): ...
    def set_progress_indicator(self, indicator: str): ...

    def print_very_verbose(self, msg: str): ...

    def flush(self): ...
