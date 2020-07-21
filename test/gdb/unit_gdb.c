/**
 * @file   unit_gdb.c
 * @date   14.07.2020
 * @author Klemens D. Morgenstern
 *
 */


#include <metal/gdb/unit.h>

#define true 1
#define false 0

int my_predicate(int i, int j) {return i == j;}

void predicate_test()
{
    METAL_ASSERT_PREDICATE(my_predicate, 4, 2);
    METAL_EXPECT_PREDICATE(my_predicate, 3, 3);
    METAL_ASSERT_PREDICATE(my_predicate, 1, 1);
    METAL_EXPECT_PREDICATE(my_predicate, 5, 2);
}


void fail_test()
{
    METAL_ASSERT(false);
}

void warn_test()
{
    METAL_EXPECT(false);
}

int canceled_func()
{
    METAL_CRITICAL(METAL_ASSERT(false), 42);
}

int critical_section()
{
    METAL_CRITICAL_SECTION(12)
    {
        METAL_ASSERT(true);
        METAL_ASSERT(false);
    }
}



void cancel_case()
{
    METAL_ASSERT_EQUAL(canceled_func(), 42);
    METAL_ASSERT_EQUAL(critical_section(), 12);

    METAL_CRITICAL(METAL_ASSERT(false));
}


void close_case()
{
    METAL_ASSERT_CLOSE(1., .9, .1);
    METAL_EXPECT_CLOSE(1., .9, .09);


    METAL_ASSERT_CLOSE_RELATIVE(2., 1.8, 0.1);
    METAL_EXPECT_CLOSE_RELATIVE(2., 1.5, 0.25);

    int a1[3] = {1,2,3};
    double a2[3] = {1.1, 1.8, 2.7};

    METAL_RANGED(a1, 3, a2, 4, METAL_ASSERT_CLOSE, 0.3);
    METAL_RANGED(a1, 3, a2, 4, METAL_EXPECT_CLOSE, 0.2);


    METAL_RANGED(a1, 3, a2, 4, METAL_ASSERT_CLOSE_RELATIVE, 0.1);
    METAL_RANGED(a1, 3, a2, 4, METAL_EXPECT_CLOSE_RELATIVE, 0.05);
}

void compare_case()
{
    METAL_ASSERT_LESSER(1, 2);
    METAL_EXPECT_LESSER(1, 1);

    METAL_ASSERT_GREATER(1, 1);
    METAL_EXPECT_GREATER(2, 1);

    int a1[3] = {1,2,3};
    int a2[3] = {3,2,1};


    METAL_RANGED(a1, 3, a2, 3, METAL_ASSERT_GREATER);
    METAL_RANGED(a1, 3, a2, 3, METAL_EXPECT_GREATER);

    METAL_RANGED(a1, 3, a2, 3, METAL_ASSERT_LESSER);
    METAL_RANGED(a1, 3, a2, 3, METAL_EXPECT_LESSER);
}

void equal_case()
{
    unsigned int i = -42;
    unsigned char j = -42;
    char k = -1;
    unsigned char l = 0xFF;

    METAL_ASSERT_EQUAL(i, j);
    METAL_EXPECT_EQUAL(l, k);

    int arr1[3] = {-1,0,1};
    short arr2[4] = {-1,0,1,2};

    METAL_RANGED(arr1, 3, arr2, 4, METAL_ASSERT_EQUAL);
    METAL_RANGED(arr1, 3, arr2, 3, METAL_EXPECT_EQUAL);

}

void ge_case()
{
    METAL_ASSERT_GE(1, 2);
    METAL_EXPECT_GE(1, 1);


    int a1[3] = {0b01,0b10,0b11};
    int a2[3] = {0b01,0b01,0b10};

    METAL_RANGED(a1, 3, a2, 3, METAL_ASSERT_GE);
    METAL_RANGED(a2, 3, a1, 3, METAL_EXPECT_GE);
}

void le_case()
{
    METAL_ASSERT_LE(1, 0);
    METAL_EXPECT_LE(1, 1);


    int a1[3] = {0b01,0b10,0b11};
    int a2[3] = {0b01,0b01,0b10};

    METAL_RANGED(a1, 3, a2, 3, METAL_ASSERT_LE);
    METAL_RANGED(a2, 3, a1, 3, METAL_EXPECT_LE);
}

void messaging_case()
{
    METAL_LOG("my log message");
    METAL_CHECKPOINT();
    METAL_ASSERT_MESSAGE(false, "Some message");
    METAL_EXPECT_MESSAGE(true,  "some other message");
    METAL_ASSERT_MESSAGE(true,  "Yet another message");
    METAL_EXPECT_MESSAGE(false, "and another one");
}

void not_equal_case()
{
    unsigned int i = -42;
    unsigned char j = -42;
    signed char k = -1;
    unsigned char l = 0xFF;

    METAL_ASSERT_NOT_EQUAL(i, j);
    METAL_EXPECT_NOT_EQUAL(l, k);

    int    arr1[3] = {-1,0,1};
    short  arr2[4] = {-1,0,1,2};

    METAL_RANGED(arr1, 3, arr2, 4, METAL_ASSERT_NOT_EQUAL);
    METAL_RANGED(arr1, 3, arr2, 3, METAL_EXPECT_NOT_EQUAL);
}

void for_case()
{
    int i = 0;
    METAL_FOR(i = 0; i < 100; i++)
    {
        METAL_EXPECT_LE(i, 5);
    }
    METAL_CHECKPOINT();
}

int main(int argc, char * argv[])
{
    METAL_CALL(predicate_test, "my predicate test case");
    METAL_CALL(fail_test);
    METAL_CALL(warn_test);
    METAL_CALL(cancel_case);
    METAL_CALL(close_case);
    METAL_CALL(compare_case);
    METAL_CALL(equal_case);
    METAL_CALL(ge_case);
    METAL_CALL(le_case);
    METAL_CALL(messaging_case);
    METAL_CALL(not_equal_case);
    METAL_CALL(for_case);

    METAL_REPORT();
    return METAL_ERROR();
}