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

#define METAL_TEST_REPORT(Type, Level, ...) METAL_SERIAL_WRITE_LOCATION(); METAL_SERIAL_WRITE_INT(METAL_PP_FIRST(__VA_ARGS__));


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
