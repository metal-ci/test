/**
 * @file   metal/gdb/unit.h
 * @date   19.07.2020
 * @author Klemens D. Morgenstern
 *
 */

#ifndef METAL_TEST_GDB_UNIT_H
#define METAL_TEST_GDB_UNIT_H

#include <metal/macros.h>
#include <metal/gdb/core.h>
#include <metal/unit.h>

#if __cplusplus >= 201103L
#define METAL_NULL nullptr
#else
#define METAL_NULL 0
#endif

enum metal_unit_level
{
    metal_unit_level_cancel,
    metal_unit_level_info,
    metal_unit_level_assert,
    metal_unit_level_expect
};

enum metal_unit_type
{
    metal_unit_type_plain,
    metal_unit_type_critical,
    metal_unit_type_critical_section,
    metal_unit_type_for,
    metal_unit_type_ranged_enter,
    metal_unit_type_ranged_exit,
    metal_unit_type_ranged,
    metal_unit_type_message,
    metal_unit_type_call_enter,
    metal_unit_type_call_exit,
    metal_unit_type_log,
    metal_unit_type_checkpoint,
    metal_unit_type_equal,
    metal_unit_type_not_equal,
    metal_unit_type_predicate,
    metal_unit_type_close,
    metal_unit_type_close_relative,
    metal_unit_type_ge,
    metal_unit_type_le,
    metal_unit_type_greater,
    metal_unit_type_lesser
};


static void metal_gdb_unit_impl(enum metal_unit_type type, enum metal_unit_level lvl, int cond_or_len,
                                const char* file, int line,
                                const char *arg0, const char *arg1, const char *arg2, const char *arg3)
{
    metal_break("metal.unit", type, lvl, cond_or_len, file, line, arg0, arg1, arg2, arg3);
}

#define METAL_TEST_REPORT_IMPL_1(Type, Level, Condition)                         metal_gdb_unit_impl(Type, Level, Condition, __FILE__, __LINE__, METAL_NULL, METAL_NULL, METAL_NULL, METAL_NULL)
#define METAL_TEST_REPORT_IMPL_2(Type, Level, Condition, Arg0)                   metal_gdb_unit_impl(Type, Level, Condition, __FILE__, __LINE__, #Arg0,      METAL_NULL, METAL_NULL, METAL_NULL)
#define METAL_TEST_REPORT_IMPL_3(Type, Level, Condition, Arg0, Arg1)             metal_gdb_unit_impl(Type, Level, Condition, __FILE__, __LINE__, #Arg0,      #Arg1,      METAL_NULL, METAL_NULL)
#define METAL_TEST_REPORT_IMPL_4(Type, Level, Condition, Arg0, Arg1, Arg2)       metal_gdb_unit_impl(Type, Level, Condition, __FILE__, __LINE__, #Arg0,      #Arg1,      #Arg2,      METAL_NULL)
#define METAL_TEST_REPORT_IMPL_5(Type, Level, Condition, Arg0, Arg1, Arg2, Arg3) metal_gdb_unit_impl(Type, Level, Condition, __FILE__, __LINE__, #Arg0,      #Arg1,      #Arg2,      #Arg3)

#define METAL_TEST_REPORT(Type, Level, ...) \
    METAL_PP_OVERLOAD(METAL_TEST_REPORT_IMPL_, __VA_ARGS__)(METAL_PP_CONCAT(metal_unit_type_,  Type), METAL_PP_CONCAT(metal_unit_level_, Level), __VA_ARGS__)

/*

METAL_TEST_REPORT(critical, cancel, 0, __FUNCTION__);
METAL_TEST_REPORT(critical, cancel, 0);
METAL_TEST_REPORT(critical, cancel, 1, __FUNCTION__);
METAL_TEST_REPORT(for, cancel, 0, for);

METAL_TEST_REPORT(ranged_enter, info, size, Lhs, LhsSize, Rhs, RhsSize);
METAL_TEST_REPORT(ranged_exit, info, i, Lhs, LhsSize, Rhs, RhsSize);
METAL_TEST_REPORT(ranged, cancel, 0);

METAL_TEST_REPORT(message, assert, Condition, Message);
METAL_TEST_REPORT(message, expect, Condition, Message);

METAL_TEST_REPORT(call_enter, info, 1, Function);
METAL_TEST_REPORT(call_enter, info, 1, Function, description)
METAL_TEST_REPORT(call_exit,  info, 1, Function);


METAL_TEST_REPORT(log, info, 1, Message)
METAL_TEST_REPORT(checkpoint, info, 1)
METAL_TEST_REPORT(equal, assert, cond, Lhs, Rhs);
METAL_TEST_REPORT(equal, expect, cond, Lhs, Rhs);

METAL_TEST_REPORT(not_equal, assert, cond, Lhs, Rhs);
METAL_TEST_REPORT(not_equal, expect, cond, Lhs, Rhs);

METAL_TEST_REPORT(predicate, assert, cond, Function, (Args));
METAL_TEST_REPORT(predicate, expect, cond, Function, (Args));

METAL_TEST_REPORT(close, assert, cond, Lhs, Rhs, Tolerance);
METAL_TEST_REPORT(close, expect, cond, Lhs, Rhs, Tolerance);

METAL_TEST_REPORT(close_relative, assert, cond, Lhs, Rhs, Tolerance);
METAL_TEST_REPORT(close_relative, expect, cond, Lhs, Rhs, Tolerance);

METAL_TEST_REPORT(ge, assert, cond, Lhs, Rhs);
METAL_TEST_REPORT(ge, expect, cond, Lhs, Rhs);

METAL_TEST_REPORT(le, assert, cond, Lhs, Rhs);
METAL_TEST_REPORT(le, expect, cond, Lhs, Rhs);

METAL_TEST_REPORT(greater, assert, cond, Lhs, Rhs);
METAL_TEST_REPORT(greater, expect, cond, Lhs, Rhs);

METAL_TEST_REPORT(lesser, assert, cond, Lhs, Rhs);
METAL_TEST_REPORT(lesser, expect, cond, Lhs, Rhs);

*/

#endif //METAL_TEST_UNIT_H
