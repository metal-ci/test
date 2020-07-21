/**
 * @file   metal/serial/unit.h
 * @date   14.07.2020
 * @author Klemens D. Morgenstern
 *
 */

#ifndef METAL_TEST_SERIAL_UNIT_H
#define METAL_TEST_SERIAL_UNIT_H

#include <metal/serial/core.h>
#include <metal/macros.h>

enum metal_unit_level
{
    metal_unit_level_cancel  = 0b00000000,
    metal_unit_level_info    = 0b00100000,
    metal_unit_level_enter   = 0b01000000,
    metal_unit_level_exit    = 0b01100000,
    metal_unit_level_assert  = 0b10000000,
    metal_unit_level_expect  = 0b10100000
};

enum metal_unit_type
{
    metal_unit_type_plain = 0,
    metal_unit_type_critical,
    metal_unit_type_critical_section,
    metal_unit_type_loop,
    metal_unit_type_ranged,
    metal_unit_type_message,
    metal_unit_type_call,
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
    metal_unit_type_lesser,
    metal_unit_type_report,
};

static const volatile int metal_serial_inline_and_reordering_prevention_thingamabob = 1;

#define METAL_TEST_REPORT_IMPL(Type, Level, Condition, Arg0, Arg1, Arg2, Arg3) if (metal_serial_inline_and_reordering_prevention_thingamabob) { METAL_SERIAL_WRITE_LOCATION(); \
    METAL_SERIAL_WRITE_BYTE(Type | Level); \
    METAL_SERIAL_WRITE_INT(Condition); }


#define METAL_TEST_REPORT_IMPL_1(Type, Level, Condition)                         METAL_TEST_REPORT_IMPL(Type, Level, Condition, , , , )
#define METAL_TEST_REPORT_IMPL_2(Type, Level, Condition, Arg0)                   METAL_TEST_REPORT_IMPL(Type, Level, Condition, #Arg0,      , , )
#define METAL_TEST_REPORT_IMPL_3(Type, Level, Condition, Arg0, Arg1)             METAL_TEST_REPORT_IMPL(Type, Level, Condition, #Arg0,      #Arg1,      , )
#define METAL_TEST_REPORT_IMPL_4(Type, Level, Condition, Arg0, Arg1, Arg2)       METAL_TEST_REPORT_IMPL(Type, Level, Condition, #Arg0,      #Arg1,      #Arg2,      )
#define METAL_TEST_REPORT_IMPL_5(Type, Level, Condition, Arg0, Arg1, Arg2, Arg3) METAL_TEST_REPORT_IMPL(Type, Level, Condition, #Arg0,      #Arg1,      #Arg2,      #Arg3)

#define METAL_TEST_REPORT(Type, Level, ...) \
    METAL_PP_OVERLOAD(METAL_TEST_REPORT_IMPL_, __VA_ARGS__)(METAL_PP_CONCAT(metal_unit_type_,  Type), METAL_PP_CONCAT(metal_unit_level_, Level), __VA_ARGS__)

#include <metal/unit.h>

/*
METAL_TEST_REPORT(critical, cancel, 0, __FUNCTION__);
METAL_TEST_REPORT(critical, cancel, 0, );
METAL_TEST_REPORT(critical, cancel, 1, __FUNCTION__);
METAL_TEST_REPORT(for, cancel, 0, for);

METAL_TEST_REPORT(ranged_enter, info, size, Lhs, LhsSize, Rhs, RhsSize);
METAL_TEST_REPORT(ranged_exit, info, i, Lhs, LhsSize, Rhs, RhsSize);
METAL_TEST_REPORT(ranged, cancel, 0, ranged);

METAL_TEST_REPORT(message, assert, Condition, Message);
METAL_TEST_REPORT(message, expect, Condition, Message);

METAL_TEST_REPORT(call_enter, info, 1, Function);
METAL_TEST_REPORT(call_enter, info, 1, Function, Description);
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
