/**
 * @file   metal/gdb/core.h
 * @date   03.07.2020
 * @author Klemens D. Morgenstern
 *
 */

#ifndef METAL_TEST_GDB_CORE_H
#define METAL_TEST_GDB_CORE_H

#define METAL_TEST_GDB 1

#if METAL_TEST_SERIAL
#error "Cannot use metal.gdb and metal.serial in the same compile unit"
#endif

#if defined(__cplusplus)
extern "C" {
#endif

void __attribute__((weak, optimize(0), noinline)) metal_break(const char* identifier __attribute__((unused)), ...)
{
    asm("");
}

#if defined(__cplusplus)
}
#endif


#endif //METAL_TEST_CORE_H
