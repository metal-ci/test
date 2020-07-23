# Newlib 

Syscall stubs are provided for both tools and are pretty straight forward to use. You need to add the syscalls.c to your compilation, 
and you can find the path like this:

```bash
metal-flags -S gdb
metal-flags -S serial
``` 

Both sources have a buffer, since newlib-nano writes byteswise, which makes semihosting very slow. The default size is 1kB, but you can configure it 
by defining `METAL_NEWLIB_BUFFER_SIZE` or disable it by defining `METAL_NEWLIB_DISABLE_BUFFER`.

## metal.gdb

metal.gdb forward all the calls to the host operating system.

## metal.serial

Metal.serial comes with three modes which you can set by defining `METAL_SERIAL_SYSCALLS_MODE` with one of the following:

### `METAL_SERIAL_SYSCALLS_MODE_BLOCKED`

This mode blocks all operations (by yielding errors) except for writing to `stdout` / `stderr`. When using the intepreter it will replicate the output.

### `METAL_SERIAL_SYSCALLS_MODE_UNCHECKED`

This is the default mode and it allows all writing operations, including opening files for writing. When using the interpreter it will replicate all those actions.


### `METAL_SERIAL_SYSCALLS_MODE_FULL`

This mode requires bidirectional mode and forward all calls to the host OS, just like metal.gdb would.