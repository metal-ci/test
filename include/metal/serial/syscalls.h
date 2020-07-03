/**
 * @file   metal/serial/syscalls.h
 * @date   03.07.2020
 * @author Klemens D. Morgenstern
 *
 */

#ifndef METAL_TEST_SERIAL_SYSCALLS_H
#define METAL_TEST_SERIAL_SYSCALLS_H

//Allow no access to any file or process, except stdout/stdin
#define METAL_SERIAL_SYSCALLS_MODE_BLOCKED 0

//Only allow writes and leaves them unchecked. This is the default.
#define METAL_SERIAL_SYSCALLS_MODE_UNCHECKED 1

//Use full I/O facilities
#define METAL_SERIAL_SYSCALLS_MODE_FULL 2

#endif //METAL_TEST_SERIAL_SYSCALLS_H
