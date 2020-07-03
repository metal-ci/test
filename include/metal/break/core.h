/**
 * @file   metal/break/core.h
 * @date   03.07.2020
 * @author Klemens D. Morgenstern
 *
 */

#ifndef METAL_TEST_BREAK_CORE_H
#define METAL_TEST_BREAK_CORE_H

#if defined(__cplusplus)
extern "C" {
#endif

void __attribute__((weak, optimize("-O0"), noinline)) metal_break(const char* identifier __attribute__((unused)), ...)
{
    asm("");
}

#if defined(__cplusplus)
}
#endif


#endif //METAL_TEST_CORE_H
