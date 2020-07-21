/**
 * @file   metal/macros.h
 * @date   01.07.2020
 * @author Klemens D. Morgenstern
 *
 */
#ifndef METAL_TEST_HOSTED_UNIT_HPP
#define METAL_TEST_HOSTED_UNIT_HPP

#include <metal/macros.h>

#if __cplusplus
#include <cstdio>
using std::printf;
#else
#include <stdio.h>
#endif

#define METAL_TEST_HOSTED 1


struct metal_unit_scope
{
    int executed;
    int errors;
    int warnings;

    int cancelled;

    struct metal_unit_scope * parent;
};

static void add_child_result(struct metal_unit_scope * parent, struct metal_unit_scope * child)
{
    parent->executed += child->executed;
    parent->errors   += child->errors;
    parent->warnings += child->warnings;
}

struct metal_unit_scope metal_unit_main_scope __attribute__((weak)) = {0,0,0, 0, METAL_NULL};
struct metal_unit_scope * metal_unit_current_scope __attribute__((weak)) = &metal_unit_main_scope;

#define METAL_TEST_REPORT_IMPL_critical(...) printf(METAL_LOCATION_STRING() " critical check failed, cancelling\n")
#define METAL_TEST_REPORT_IMPL_loop(...) printf(METAL_LOCATION_STRING() " for loop cancelled\n")

#define METAL_TEST_REPORT_IMPL_STAT_assert() metal_unit_current_scope->errors++
#define METAL_TEST_REPORT_IMPL_STAT_expect() metal_unit_current_scope->warnings++
#define METAL_TEST_REPORT_IMPL_STAT(Level, Condition) metal_unit_current_scope->executed++; if (Condition) METAL_PP_CONCAT(METAL_TEST_REPORT_IMPL_STAT_, Level) () ;

#define METAL_TEST_REPORT_IMPL_ranged_info_str(Lhs, Lhs_Len, Rhs, Rhs_Len) #Lhs "[0 ... " #Lhs_Len "] and " #Rhs "[0 ...  " Rhs_Len "]"
#define METAL_TEST_REPORT_IMPL_ranged_cancel(Condition_Or_Length) printf(METAL_LOCATION_STRING() " ranged test cancelled at pos %d\n", Condition_Or_Length)
#define METAL_TEST_REPORT_IMPL_ranged_exit(Level, Lhs, Lhs_Len, Rhs, Rhs_Len)   printf(METAL_LOCATION_STRING() " ranged test completed with %d elements\n", Level)
#define METAL_TEST_REPORT_IMPL_ranged_enter(Level, Lhs, Lhs_Len, Rhs, Rhs_Len)  printf(METAL_LOCATION_STRING() " ranged test starting with %d elements for "  #Lhs "[0 ... " #Lhs_Len "] and " #Rhs "[0 ...  " #Rhs_Len "]" "\n", Level)

#define METAL_TEST_REPORT_IMPL_ranged(Level, ...)  METAL_PP_CONCAT(METAL_TEST_REPORT_IMPL_ranged_, Level) ( __VA_ARGS__ )

#define METAL_TEST_REPORT_IMPL_call_descriptor_1(Func) #Func
#define METAL_TEST_REPORT_IMPL_call_descriptor_2(Func, Descriptor) Descriptor

#define METAL_TEST_REPORT_IMPL_call_enter(Condition_Or_Length, ...)   \
    printf(METAL_LOCATION_STRING() " entering test case %s\n", METAL_PP_OVERLOAD(METAL_TEST_REPORT_IMPL_call_descriptor_, __VA_ARGS__) (__VA_ARGS__)); \
    struct metal_unit_scope METAL_PP_CONCAT(test_case_, __LINE__) = {0, 0, 0, 0, metal_unit_current_scope}; \
    metal_unit_current_scope = &METAL_PP_CONCAT(test_case_, __LINE__);

#define METAL_TEST_REPORT_IMPL_call_exit(Condition_Or_Length, ...)  \
    printf(METAL_LOCATION_STRING() " %s test case %s, %s with {executed: %d, warnings: %d, errors: %d}\n", \
            metal_unit_current_scope->cancelled ? "cancelled" : "exiting", \
            METAL_PP_OVERLOAD(METAL_TEST_REPORT_IMPL_call_descriptor_, __VA_ARGS__) (__VA_ARGS__), \
            metal_unit_current_scope->errors ? "succeeded" : "failed", \
            metal_unit_current_scope->executed,  metal_unit_current_scope->warnings, metal_unit_current_scope->errors); \
    add_child_result(metal_unit_current_scope->parent, metal_unit_current_scope); \
    metal_unit_current_scope = metal_unit_current_scope->parent; \

#define METAL_TEST_REPORT_IMPL_call(Level, ...)  METAL_PP_CONCAT(METAL_TEST_REPORT_IMPL_call_, Level) ( __VA_ARGS__ )

#define METAL_TEST_REPORT_IMPL_log(Level, Condition, Arg) printf(METAL_LOCATION_STRING() " log : " Arg "\n")
#define METAL_TEST_REPORT_IMPL_checkpoint(...) printf(METAL_LOCATION_STRING() " checkpoint\n")

#define METAL_TEST_REPORT_IMPL_plain(Level, Condition, Description)   METAL_TEST_REPORT_IMPL_STAT(Level, Condition); printf(METAL_LOCATION_STRING() " [plain]: " #Description " " #Level " %s\n", Condition ? "succeeded " : "failed ")
#define METAL_TEST_REPORT_IMPL_message(Level, Condition, Description) METAL_TEST_REPORT_IMPL_STAT(Level, Condition); printf(METAL_LOCATION_STRING() " [message]: " Description " " #Level " %s\n", Condition ? "succeeded " : "failed ")
#define METAL_TEST_REPORT_IMPL_equal(Level, Condition, Lhs, Rhs)      METAL_TEST_REPORT_IMPL_STAT(Level, Condition); printf(METAL_LOCATION_STRING() " [equal]: " #Lhs " == " #Rhs " " #Level " %s\n", Condition ? "succeeded " : "failed ")
#define METAL_TEST_REPORT_IMPL_not_equal(Level, Condition, Lhs, Rhs)  METAL_TEST_REPORT_IMPL_STAT(Level, Condition); printf(METAL_LOCATION_STRING() " [not_equal]: " #Lhs " != " #Rhs " " #Level " %s\n", Condition ? "succeeded " : "failed ")
#define METAL_TEST_REPORT_IMPL_ge(Level, Condition, Lhs, Rhs)         METAL_TEST_REPORT_IMPL_STAT(Level, Condition); printf(METAL_LOCATION_STRING() " [ge]: " #Lhs " >= " #Rhs " " #Level " %s\n", Condition ? "succeeded " : "failed ")
#define METAL_TEST_REPORT_IMPL_le(Level, Condition, Lhs, Rhs)         METAL_TEST_REPORT_IMPL_STAT(Level, Condition); printf(METAL_LOCATION_STRING() " [le]: " #Lhs " <= " #Rhs " " #Level " %s\n", Condition ? "succeeded " : "failed ")
#define METAL_TEST_REPORT_IMPL_greater(Level, Condition, Lhs, Rhs)    METAL_TEST_REPORT_IMPL_STAT(Level, Condition); printf(METAL_LOCATION_STRING() " [greater]: " #Lhs " > " #Rhs " " #Level " %s\n", Condition ? "succeeded " : "failed ")
#define METAL_TEST_REPORT_IMPL_lesser(Level, Condition, Lhs, Rhs)     METAL_TEST_REPORT_IMPL_STAT(Level, Condition); printf(METAL_LOCATION_STRING() " [lesser]: " #Lhs " < " #Rhs " " #Level " %s\n", Condition ? "succeeded " : "failed ")

#define METAL_TEST_REPORT_IMPL_close(Level, Condition, Lhs, Rhs, Tolerance)           METAL_TEST_REPORT_IMPL_STAT(Level, Condition); printf(METAL_LOCATION_STRING() " [close]: " #Lhs " == " #Rhs " +/- " #Tolerance " "#Level " %s\n", Condition ? "succeeded " : "failed ")
#define METAL_TEST_REPORT_IMPL_close_relative(Level, Condition, Lhs, Rhs, Tolerance)  METAL_TEST_REPORT_IMPL_STAT(Level, Condition); printf(METAL_LOCATION_STRING() " [close_relative]: " #Lhs " == " #Rhs " ~ " #Tolerance " "#Level " %s\n", Condition ? "succeeded " : "failed ")
#define METAL_TEST_REPORT_IMPL_predicate(Level, Condition, Function, Args)            METAL_TEST_REPORT_IMPL_STAT(Level, Condition); printf(METAL_LOCATION_STRING() " [predicate]: " #Function #Args "\n")


#define METAL_TEST_REPORT_IMPL_report(Level, Arg) printf(METAL_LOCATION_STRING() " full test report: {executed: %d, warnings: %d, errors: %d}\n", metal_unit_main_scope.executed, metal_unit_main_scope.warnings, metal_unit_main_scope.errors)

#define METAL_TEST_REPORT_IMPL_1(Type, Level, Condition)                         TEST_PRINT(Type, Level, Condition, __FILE__, __LINE__)
#define METAL_TEST_REPORT_IMPL_2(Type, Level, Condition, Arg0)                   TEST_PRINT(Type, Level, Condition, __FILE__, __LINE__, #Arg0)
#define METAL_TEST_REPORT_IMPL_3(Type, Level, Condition, Arg0, Arg1)             TEST_PRINT(Type, Level, Condition, __FILE__, __LINE__, #Arg0,      #Arg1)
#define METAL_TEST_REPORT_IMPL_4(Type, Level, Condition, Arg0, Arg1, Arg2)       TEST_PRINT(Type, Level, Condition, __FILE__, __LINE__, #Arg0,      #Arg1,      #Arg2)
#define METAL_TEST_REPORT_IMPL_5(Type, Level, Condition, Arg0, Arg1, Arg2, Arg3) TEST_PRINT(Type, Level, Condition, __FILE__, __LINE__, #Arg0,      #Arg1,      #Arg2,      #Arg3)


//METAL_LOCATION_STRING()

//#define METAL_TEST_REPORT(Type, Level, ...) \
  //  METAL_PP_OVERLOAD(METAL_TEST_REPORT_IMPL_, __VA_ARGS__)(METAL_PP_CONCAT(metal_unit_type_,  Type), METAL_PP_CONCAT(metal_unit_level_, Level), __VA_ARGS__)

#define METAL_TEST_REPORT(Type, ...) \
    METAL_PP_CONCAT(METAL_TEST_REPORT_IMPL_, Type) ( __VA_ARGS__ )
    //printf(__FILE__ "(" METAL_PP_STRINGIFY(__LINE__) ") " METAL_PP_STRINGIFY(Type) " > " METAL_PP_STRINGIFY(Level) " : %d, with " #__VA_ARGS__ "\n", Condition);

#include <metal/unit.h>

#endif //METAL_TEST_UNIT_HPP
