#ifndef METAL_TEST_CPPUTEST_HPP
#define METAL_TEST_CPPUTEST_HPP

#include <CppUTest/TestOutput.h>
#include <CppUTest/TestRegistry.h>

extern "C" void metal_serial_write(char c);

namespace metal
{

namespace serial
{

struct CppUTestOutput : TestOutput
{
    void printTestsStarted() override;
    void printTestsEnded(const TestResult& result) override;
    void printCurrentTestStarted(const UtestShell& test) override;
    void printCurrentTestEnded(const TestResult& res) override;
    void printCurrentGroupStarted(const UtestShell& test) override;
    void printCurrentGroupEnded(const TestResult& res) override;

    void verbose(VerbosityLevel level) override;
    void color() override;
    void printBuffer(const char*) override;
    void print(const char*) override;
    void print(long) override;
    void print(size_t) override;
    void printDouble(double) override;
    void printFailure(const TestFailure& failure) override;
    void printTestRun(size_t number, size_t total) override;
    void setProgressIndicator(const char*) override;

    void printVeryVerbose(const char*) override;

    void flush() override;
};


bool RunAllTests(TestRegistry * registry = TestRegistry::getCurrentRegistry());

}

}

#endif //METAL_TEST_CPPUTEST_HPP
