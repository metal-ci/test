/**
 * @file   metal/unit.h
 * @date   15.07.2020
 * @author Klemens D. Morgenstern
 *
 */
#ifndef METAL_TEST_UNIT_H
#define METAL_TEST_UNIT_H

#include <metal/macros.h>


#if __cplusplus
#include <cstring>
#include <cstdint>
typedef bool metal_bool;
#else
#include <string.h>
#include <stdint.h>
typedef int metal_bool;
#endif



#if !METAL_TEST_GDB && !METAL_TEST_SERIAL && !defined(METAL_TEST_REPORT)
#warning "You are using metal.test without serial, gdb and a custom METAL_TEST_REPORT macro - you will get now test reporting"
#define METAL_TEST_REPORT(...)
#endif

const static void * metal_error_label = 0;

#define METAL_ENTER_CRITICAL_SECTION() \
    const void * metal_error_label = && METAL_PP_CONCAT(metal_error_label, __LINE__); \
    goto METAL_PP_CONCAT(metal_section_label, __LINE__); \
    METAL_PP_CONCAT(metal_error_label, __LINE__): \
    METAL_TEST_REPORT(critical, cancel  0, __FUNCTION__); \
    return Result ; \
    METAL_PP_CONCAT(metal_section_label, __LINE__): \


#define METAL_CRITICAL_2(Assertion, Result) \
    {const void * metal_error_label = && METAL_PP_CONCAT(metal_error_label, __LINE__); \
     goto METAL_PP_CONCAT(metal_section_label, __LINE__); \
     METAL_PP_CONCAT(metal_error_label, __LINE__): \
     METAL_TEST_REPORT(critical, cancel, 0); \
     return Result ; \
     METAL_PP_CONCAT(metal_section_label, __LINE__): \
     Assertion; }

#define METAL_CRITICAL_1(Assertion) METAL_CRITICAL_2(Assertion, )
#define METAL_CRITICAL(...) METAL_PP_OVERLOAD(METAL_CRITICAL_, __VA_ARGS__)(__VA_ARGS__)

#if (__STDC_VERSION__ >= 199901L) || defined(__cplusplus) || __PCPP_ALWAYS_TRUE__

#define METAL_CRITICAL_SECTION(Result) \
    goto METAL_PP_CONCAT(metal_section_label, __LINE__); \
    METAL_PP_CONCAT(metal_error_label, __LINE__): \
    METAL_TEST_REPORT(critical, cancel, 0); \
    return Result ; \
    METAL_PP_CONCAT(metal_section_label, __LINE__): \
    for (const void * metal_error_label = && METAL_PP_CONCAT(metal_error_label, __LINE__); metal_error_label; metal_error_label = 0)

#define METAL_FOR(...) \
    const void * outer_error_label = metal_error_label;        \
    const void * metal_error_label = && METAL_PP_CONCAT(metal_error_label, __LINE__); \
    goto METAL_PP_CONCAT(metal_for_label_, __LINE__); \
    METAL_PP_CONCAT(metal_error_label, __LINE__): \
    METAL_TEST_REPORT(loop, cancel, 0, __FUNCTION__); \
    metal_error_label = outer_error_label ; \
    METAL_PP_CONCAT(metal_for_label_, __LINE__): \
    for (; metal_error_label ==  && METAL_PP_CONCAT(metal_error_label, __LINE__); metal_error_label = metal_error_label) \
        for (__VA_ARGS__)


#endif

//METAL_TEST_REPORT

#define METAL_RANGED_INVOKE_1(Lhs, Rhs, Macro) Macro(Lhs, Rhs)
#define METAL_RANGED_INVOKE_2(Lhs, Rhs, Macro, ...) Macro(Lhs, Rhs, __VA_ARGS__)
#define METAL_RANGED_INVOKE_3(Lhs, Rhs, Macro, ...) Macro(Lhs, Rhs, __VA_ARGS__)
#define METAL_RANGED_INVOKE_4(Lhs, Rhs, Macro, ...) Macro(Lhs, Rhs, __VA_ARGS__)
#define METAL_RANGED_INVOKE_5(Lhs, Rhs, Macro, ...) Macro(Lhs, Rhs, __VA_ARGS__)
#define METAL_RANGED_INVOKE_6(Lhs, Rhs, Macro, ...) Macro(Lhs, Rhs, __VA_ARGS__)
#define METAL_RANGED_INVOKE_7(Lhs, Rhs, Macro, ...) Macro(Lhs, Rhs, __VA_ARGS__)

#define METAL_RANGED(Lhs, LhsSize, Rhs, RhsSize, MACRO...) \
{                                                               \
    int status = 1;                                             \
    int i = 0;                                                  \
    const size_t size = LhsSize > RhsSize ? RhsSize : LhsSize;  \
    METAL_TEST_REPORT(ranged, enter, size, Lhs, LhsSize, Rhs, RhsSize); \
                                                                \
    const void * outer_error_label = metal_error_label;         \
    goto METAL_PP_CONCAT(metal_section_label, __LINE__);        \
    METAL_PP_CONCAT(metal_error_label, __LINE__):               \
    METAL_TEST_REPORT(ranged, cancel, 1);                       \
    if (metal_error_label)                                      \
        goto *metal_error_label;                                \
    else                                                        \
        goto METAL_PP_CONCAT(metal_range_end_label, __LINE__);  \
    METAL_PP_CONCAT(metal_section_label, __LINE__):             \
                                                                \
    for (const void * metal_error_label = && METAL_PP_CONCAT(metal_error_label, __LINE__); metal_error_label ==  && METAL_PP_CONCAT(metal_error_label, __LINE__); metal_error_label = outer_error_label) \
            for (i =0; i < size; i++)                                              \
            METAL_PP_OVERLOAD(METAL_RANGED_INVOKE_, MACRO)(Lhs[i], Rhs[i], MACRO); \
                                                                                   \
METAL_PP_CONCAT(metal_range_end_label, __LINE__) :                                 \
    METAL_TEST_REPORT(ranged, exit, i, Lhs, LhsSize, Rhs, RhsSize);           \
}

metal_bool __attribute__((weak)) metal_test_errored = 1;
#define METAL_ERROR() +metal_test_errored

#define METAL_REPORT()  METAL_TEST_REPORT(report, info, metal_test_errored > 0)

#define METAL_ASSERT_IMPL(Condition) { metal_test_errored |= Condition;  if (!Condition && metal_error_label) goto *metal_error_label;}
#define METAL_EXPECT_IMPL(Condition) { if (!Condition && metal_error_label) goto *metal_error_label; }

#define METAL_ASSERT(Condition) { int cond = Condition ? 1 : 0; METAL_TEST_REPORT(plain, assert, cond, #Condition); METAL_ASSERT_IMPL(cond); }
#define METAL_EXPECT(Condition) { int cond = Condition ? 1 : 0; METAL_TEST_REPORT(plain, expect, cond, #Condition); METAL_EXPECT_IMPL(cond); }

#define METAL_ASSERT_MESSAGE(Condition, Message) { int cond = Condition ? 1 : 0;  METAL_TEST_REPORT(message, assert, Condition, Message); METAL_ASSERT_IMPL(cond); }
#define METAL_EXPECT_MESSAGE(Condition, Message) { int cond = Condition ? 1 : 0;  METAL_TEST_REPORT(message, expect, Condition, Message); METAL_EXPECT_IMPL(cond); }

#define METAL_CALL_1(Function)              {                                        METAL_TEST_REPORT(call, enter, 1, Function); Function();              METAL_TEST_REPORT(call, exit, METAL_ERROR(), Function); }
#define METAL_CALL_2(Function, Description) { const char *description = Description; METAL_TEST_REPORT(call, enter, 1, Function, Description); Function(); METAL_TEST_REPORT(call, exit, METAL_ERROR(), Function); }
#define METAL_CALL(...) METAL_PP_OVERLOAD(METAL_CALL_, __VA_ARGS__)(__VA_ARGS__)

#define METAL_LOG(Message) METAL_TEST_REPORT(log, info, 1, Message)
#define METAL_CHECKPOINT() METAL_TEST_REPORT(checkpoint, info, 1)

#define METAL_ASSERT_EQUAL(Lhs, Rhs) { int cond = (Lhs == METAL_PP_FIRST(Rhs)) ? 1 : 0; METAL_TEST_REPORT(equal, assert, cond, Lhs, Rhs); METAL_ASSERT_IMPL(cond); }
#define METAL_EXPECT_EQUAL(Lhs, Rhs) { int cond = (Lhs == METAL_PP_FIRST(Rhs)) ? 1 : 0; METAL_TEST_REPORT(equal, expect, cond, Lhs, Rhs); METAL_EXPECT_IMPL(cond); }

#define METAL_ASSERT_NOT_EQUAL(Lhs, Rhs) { int cond = (Lhs != METAL_PP_FIRST(Rhs)) ? 1 : 0; METAL_TEST_REPORT(not_equal, assert, cond, Lhs, Rhs); METAL_ASSERT_IMPL(cond); }
#define METAL_EXPECT_NOT_EQUAL(Lhs, Rhs) { int cond = (Lhs != METAL_PP_FIRST(Rhs)) ? 1 : 0; METAL_TEST_REPORT(not_equal, expect, cond, Lhs, Rhs); METAL_EXPECT_IMPL(cond); }

#define METAL_ASSERT_GE(Lhs, Rhs) { int cond = (Lhs >= METAL_PP_FIRST(Rhs)) ? 1 : 0; METAL_TEST_REPORT(ge, assert, cond, Lhs, Rhs); METAL_ASSERT_IMPL(cond); }
#define METAL_EXPECT_GE(Lhs, Rhs) { int cond = (Lhs >= METAL_PP_FIRST(Rhs)) ? 1 : 0; METAL_TEST_REPORT(ge, expect, cond, Lhs, Rhs); METAL_EXPECT_IMPL(cond); }

#define METAL_ASSERT_LE(Lhs, Rhs) { int cond = (Lhs <= METAL_PP_FIRST(Rhs)) ? 1 : 0; METAL_TEST_REPORT(le, assert, cond, Lhs, Rhs); METAL_ASSERT_IMPL(cond); }
#define METAL_EXPECT_LE(Lhs, Rhs) { int cond = (Lhs <= METAL_PP_FIRST(Rhs)) ? 1 : 0; METAL_TEST_REPORT(le, expect, cond, Lhs, Rhs); METAL_EXPECT_IMPL(cond); }

#define METAL_ASSERT_GREATER(Lhs, Rhs) { int cond = (Lhs > METAL_PP_FIRST(Rhs)) ? 1 : 0; METAL_TEST_REPORT(greater, assert, cond, Lhs, Rhs); METAL_ASSERT_IMPL(cond); }
#define METAL_EXPECT_GREATER(Lhs, Rhs) { int cond = (Lhs > METAL_PP_FIRST(Rhs)) ? 1 : 0; METAL_TEST_REPORT(greater, expect, cond, Lhs, Rhs); METAL_EXPECT_IMPL(cond); }

#define METAL_ASSERT_LESSER(Lhs, Rhs) { int cond = (Lhs < METAL_PP_FIRST(Rhs)) ? 1 : 0; METAL_TEST_REPORT(lesser, assert, cond, Lhs, Rhs); METAL_ASSERT_IMPL(cond); }
#define METAL_EXPECT_LESSER(Lhs, Rhs) { int cond = (Lhs < METAL_PP_FIRST(Rhs)) ? 1 : 0; METAL_TEST_REPORT(lesser, expect, cond, Lhs, Rhs); METAL_EXPECT_IMPL(cond); }

#define METAL_ASSERT_PREDICATE(Function, Args...) { int cond = Function( Args ) ? 1 : 0; METAL_TEST_REPORT(predicate, assert, cond, Function, (Args)); METAL_ASSERT_IMPL(cond); }
#define METAL_EXPECT_PREDICATE(Function, Args...) { int cond = Function( Args ) ? 1 : 0; METAL_TEST_REPORT(predicate, expect, cond, Function, (Args)); METAL_EXPECT_IMPL(cond); }

#define METAL_ASSERT_CLOSE(Lhs, Rhs, Tolerance) { int cond = ((Rhs <= (Lhs + Tolerance)) && (Rhs >= (Lhs - Tolerance))) ? 1 : 0; METAL_TEST_REPORT(close, assert, cond, Lhs, Rhs, Tolerance); METAL_ASSERT_IMPL(cond); }
#define METAL_EXPECT_CLOSE(Lhs, Rhs, Tolerance) { int cond = ((Rhs <= (Lhs + Tolerance)) && (Rhs >= (Lhs - Tolerance))) ? 1 : 0; METAL_TEST_REPORT(close, expect, cond, Lhs, Rhs, Tolerance); METAL_EXPECT_IMPL(cond); }

#define METAL_ASSERT_CLOSE_RELATIVE(Lhs, Rhs, Tolerance) {int cond = ((Rhs <= (Lhs * (1. + Tolerance))) && (Rhs >= (Lhs * (1. - Tolerance)))) ? 1 : 0; METAL_TEST_REPORT(close_relative, assert, cond, Lhs, Rhs, Tolerance); METAL_ASSERT_IMPL(cond); }
#define METAL_EXPECT_CLOSE_RELATIVE(Lhs, Rhs, Tolerance) {int cond = ((Rhs <= (Lhs * (1. + Tolerance))) && (Rhs >= (Lhs * (1. - Tolerance)))) ? 1 : 0; METAL_TEST_REPORT(close_relative, expect, cond, Lhs, Rhs, Tolerance); METAL_EXPECT_IMPL(cond); }

#endif //METAL_TEST_UNIT_H
