/**
 * @file   catch_hosted.cpp
 * @date   20.07.2020
 * @author Klemens D. Morgenstern
 *
 */


#include <metal/macros.h>
#include <cstdio>


#define METAL_UNIT_MAIN
#include <metal/serial/unit.h>
#include <metal/unit.h>

void metal_serial_write(char c) { fputc(c, stdout);}

void __attribute__((constructor)) init_stdout()
{
    freopen(NULL, "wb", stdout);

    setvbuf(stdout, NULL, _IONBF, 0);
}

using metal::unit::operator""_eps;

int my_predicate(int i, int j) {return i == j;}

METAL_CASE("predicate test")
{
    METAL_ASSERT(my_predicate(4, 2));
    METAL_ASSERT(my_predicate(3, 3));
    METAL_ASSERT(my_predicate(1, 1));
    METAL_ASSERT(my_predicate(5, 2));
}


METAL_CASE("failed test")
{
    METAL_ASSERT(false);
}

METAL_CASE("warn test")
{
    METAL_ASSERT(false);
}

METAL_CASE("cancel case")
{
    METAL_EXPECT(false);
}


METAL_CASE("close case")
{
    METAL_ASSERT(1. == .9 +- 1_eps);
    METAL_ASSERT(1. == .9 +- .09_eps);
//
//
    METAL_ASSERT(2. == 1.8 +- ~0.1_eps);
    METAL_ASSERT(2. == 1.5 +- ~0.25_eps);
}

METAL_CASE("compare case")
{
    METAL_ASSERT(1 < 2);
    METAL_ASSERT(1 < 1);

    METAL_ASSERT(1 > 1);
    METAL_ASSERT(2 > 1);

}

METAL_CASE("equal case")
{
    unsigned int i = -42;
    unsigned char j = -42;
    char k = -1;
    unsigned char l = 0xFF;

    METAL_ASSERT(i == j);
    METAL_ASSERT(l == k);
}

METAL_CASE("ge case")
{
    METAL_ASSERT(1 >= 2);
    METAL_ASSERT(1 >= 1);
}

METAL_CASE("le case")
{
    METAL_ASSERT(1 <= 0);
    METAL_ASSERT(1 <= 1);
}

METAL_CASE("not equal case")
{
    unsigned int i = -42;
    unsigned char j = -42;
    signed char k = -1;
    unsigned char l = 0xFF;

    METAL_ASSERT(i != j);
    METAL_ASSERT(l != k);
}