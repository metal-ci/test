#include <metal/serial/cpputest.hpp>
#include <metal/serial/core.h>
#include <CppUTest/TestResult.h>
#include <CppUTest/TestFailure.h>
#include <CppUTest/Utest.h>


namespace metal
{

namespace serial
{

#define METAL_SERIAL_CPPUTEST(...) METAL_SERIAL_WRITE_LOCATION()

namespace
{

void printImpl(const SimpleString &str)
{
    const char *val = str.asCharString();
    METAL_SERIAL_WRITE_STR(val);
}

void printImpl(bool b)
{
    METAL_SERIAL_WRITE_BYTE(b ? 1 : 0);
}

void printImpl(const TestResult &result)
{
    auto p = [](auto i) METAL_SERIAL_WRITE_INT(i);
    p(result.getTestCount());
    p(result.getRunCount());
    p(result.getCheckCount());
    p(result.getFilteredOutCount());
    p(result.getIgnoredCount());
    p(result.getFailureCount());
    p(result.getTotalExecutionTime());
    p(result.getCurrentTestTotalExecutionTime());
    p(result.getCurrentGroupTotalExecutionTime());
}

void printImpl(const UtestShell &s)
{
    printImpl(s.getName());
    printImpl(s.getGroup());
    printImpl(s.getFormattedName());
    printImpl(s.getFile());

    size_t lineNumber = s.getLineNumber();
    METAL_SERIAL_WRITE_INT(lineNumber);
}

void printImpl(const TestFailure &failure)
{

    printImpl(failure.getFileName());
    printImpl(failure.getTestName());
    printImpl(failure.getTestNameOnly());

    size_t failureLineNumber = failure.getFailureLineNumber();
    METAL_SERIAL_WRITE_INT(failureLineNumber);

    printImpl(failure.getMessage());
    printImpl(failure.getTestFileName());

    size_t testLineNumber = failure.getTestLineNumber();
    METAL_SERIAL_WRITE_INT(testLineNumber);

    printImpl(failure.isOutsideTestFile());
    printImpl(failure.isInHelperFunction());
}

}

void CppUTestOutput::printTestsStarted()
{
    METAL_SERIAL_CPPUTEST(printTestsStarted);
}

void CppUTestOutput::printTestsEnded(const TestResult &result)
{
    METAL_SERIAL_CPPUTEST(printTestsEnded);
    printImpl(result);

}

void CppUTestOutput::printCurrentTestStarted(const UtestShell &test)
{
    METAL_SERIAL_CPPUTEST(printCurrentTestStarted);
    printImpl(test);
}

void CppUTestOutput::printCurrentTestEnded(const TestResult &res)
{
    METAL_SERIAL_CPPUTEST(printCurrentTestEnded);
    printImpl(res);
}

void CppUTestOutput::printCurrentGroupStarted(const UtestShell &test)
{
    METAL_SERIAL_CPPUTEST(printCurrentGroupStarted);
    printImpl(test);
}

void CppUTestOutput::printCurrentGroupEnded(const TestResult &res)
{
    METAL_SERIAL_CPPUTEST(printCurrentGroupEnded);
    printImpl(res);
}

void CppUTestOutput::verbose(VerbosityLevel level)
{
    METAL_SERIAL_CPPUTEST(verbose);

    switch (level)
    {
        case level_quiet:
            METAL_SERIAL_WRITE_BYTE((char) 0);
            break;
        case level_verbose:
            METAL_SERIAL_WRITE_BYTE((char) 1);
            break;
        case level_veryVerbose:
            METAL_SERIAL_WRITE_BYTE((char) 2);
            break;
    }
}

void CppUTestOutput::color()
{
    METAL_SERIAL_CPPUTEST(color);
}

void CppUTestOutput::printBuffer(const char *buf)
{
    METAL_SERIAL_CPPUTEST(printBuffer);
    METAL_SERIAL_WRITE_STR(buf);
}

void CppUTestOutput::print(const char *buf)
{
    METAL_SERIAL_CPPUTEST(print, str);
    METAL_SERIAL_WRITE_STR(buf);
}

void CppUTestOutput::print(long value)
{
    METAL_SERIAL_CPPUTEST(print, int);
    METAL_SERIAL_WRITE_INT(value);
}

void CppUTestOutput::print(size_t value)
{
    METAL_SERIAL_CPPUTEST(print, int);
    METAL_SERIAL_WRITE_INT(value);
}

void CppUTestOutput::printDouble(double d)
{
    METAL_SERIAL_CPPUTEST(print, double);
    printImpl(StringFrom(d));
}

void CppUTestOutput::printFailure(const TestFailure &failure)
{
    METAL_SERIAL_CPPUTEST(printFailure);
    printImpl(failure);
}

void CppUTestOutput::printTestRun(size_t number, size_t total)
{
    METAL_SERIAL_CPPUTEST(printTestRun);
    METAL_SERIAL_WRITE_INT(number);
    METAL_SERIAL_WRITE_INT(total);
}

void CppUTestOutput::setProgressIndicator(const char *progressIndicator)
{
    METAL_SERIAL_CPPUTEST(setProgressIndicator);
    METAL_SERIAL_WRITE_STR(progressIndicator);
}

void CppUTestOutput::printVeryVerbose(const char *msg)
{
    METAL_SERIAL_CPPUTEST(setProgressIndicator);
    METAL_SERIAL_WRITE_STR(msg);
}

void CppUTestOutput::flush()
{
    METAL_SERIAL_CPPUTEST(flush);
}

bool RunAllTests(TestRegistry * registry)
{
    CppUTestOutput output;
    TestResult tr(output);

    registry->runAllTests(tr);

    return !tr.isFailure();
}

}

}