![CI](https://github.com/metal-ci/test/workflows/CI/badge.svg?branch=master) [![Issues](https://img.shields.io/github/issues/metal-ci/test.svg)](https://github.com/metal-ci/test/issues)

# About

This framework provides facilities for automated execution of remote code. The core idea is, to utilize the debug symbols for automated testing, instead of developing custom tools. 
It does however limit some things to the itanium abi, i.e. gcc and clang.

At the current state it provides functionality for:
 
 * [Exit code propagation](https://github.com/metal-ci/doc/readme.md) 
 * [Unit testing](https://github.com/metal-ci/doc/unit.md)
 * [Syscall stubs](https://github.com/metal-ci/doc/newlib.md)
 * [Argument assignment](https://github.com/metal-ci/doc/argv.md)
 
All tooling is written in python and easily extensible. Almost everything is written in C89, but we also have some modern C++ features. 

# Tool Overview

## [metal.gdb](https://github.com/metal-ci/test/doc/metal.gdb.md)

The metal.gdb tool is the core. It uses the [Python API](https://sourceware.org/gdb/onlinedocs/gdb/Python-API.html) of gdb to run code and obtain detailed information.
This allows us to analyse and print values during unit tests without any allocations. Our toolset wraps around this and uses a single breakpoint to provide a variety of functionality, all written as plugins.

Since it is gdb based you can use it with any of those targets:

 * local execution
 * remote server (*gdbsever*)
 * [openocd](http://openocd.org/)
 * [qemu](http://www.qemu.org/)

Since everything is a gdb plugin, you can use any of the functionality during a debug session, not only standalone.

## [metal.serial](https://github.com/metal-ci/test/doc/metal.serial.md)

The serial library provides a light-weight testing tool for environments that do not provide access for a debugger. It does utilize debug symbols, but to a minimal degree.
The debug symbols are used in conjunction with a preprocessor to conveniently generate you a binary protocol for uni- or bidirectional communication with the target device, e.g. through a serial port.
All you need is a function to write (and maybe receive) bytes you can enjoy the same features as `metal.gdb`, but without the introspectio.

I wrote two articles so far about how metal.serial works.
    
 * [Line Information Without Strings](https://embeddedartistry.com/blog/2020/06/29/metal-serial-capturing-file-line-information-without-using-strings/)
 * [ELFs & DWARFs](https://embeddedartistry.com/blog/2020/07/13/metal-serial-elfs-dwarfs/)  

# Getting started

`metal.test` is shipped as a `pip` package, since most is in python.

```bash
pip install metal_test
```

The `metal-flags` tool allows you get the compiler flags, which you could for example use in your CMake build through `execute_process`.

```bash
metal-flags -I -S gdb
```

# Documentation

The current master Documentation can be found in the [wiki](https://github.com/metal-ci/test/doc).


