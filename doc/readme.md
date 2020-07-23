# metal.test

Metal.test can be used in three ways:

 * [gdb](metal.gdb.md)
 * [serial](metal.serial.md)
 * hosted
 
The gdb-mode will use the gdb with our plugins, serial will utilize the serial tool and byte stream you need to provide and hosted will allow the code to be run
on a machine with an operating system. The latter is only needed for the [unit](unit.md) library, since all other functionality is provided by the operating system.  

# How to read the documentation

Both tools have separate chapters documentation that are recommended for study for writing your own extensions.

 * [gdb](metal.gdb.md)
 * [serial](metal.serial.md)

Every of the components does bring minimal code examples for both tools, as well. 

 * [Exit code propagation](https://github.com/metal-ci/doc/exit-code.md) 
 * [Unit testing](https://github.com/metal-ci/doc/unit.md)
 * [Syscall stubs](https://github.com/metal-ci/doc/newlib.md)
 * [Argument assignment](https://github.com/metal-ci/doc/argv.md)

