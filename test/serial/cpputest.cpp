#include <CppUTest/TestHarness.h>
#include <metal/serial/cpputest.hpp>
#include <CppUTest/CommandLineTestRunner.h>
#include <metal/serial/core.h>


TEST_GROUP(FirstTestGroup)
{
};

TEST(FirstTestGroup, SecondTest)
{
    STRCMP_EQUAL("hello", "world");
    LONGS_EQUAL(1, 2);
    CHECK(false);
}

void metal_serial_write(char c) { fputc(c, stdout);}

int main(int argc, char ** args)
{
    freopen(NULL, "wb", stdout);
    setvbuf(stdout, NULL, _IONBF, 0);

    METAL_SERIAL_INIT();

    int res = metal::serial::RunAllTests() ? 0 : 1;

    METAL_SERIAL_EXIT(res);
    return res;
}