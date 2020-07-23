# metal.serial

Metal.serial reads the binary and it's source code and generates a json file with the expected output that is then intepreted after you run it.  

You can find more details on how this works here:   

 * [Line Information Without Strings](https://embeddedartistry.com/blog/2020/06/29/metal-serial-capturing-file-line-information-without-using-strings/)
 * [ELFs & DWARFs](https://embeddedartistry.com/blog/2020/07/13/metal-serial-elfs-dwarfs/)  

## Code requirements

To use metal.serial, you need to initialize it first, with `METAL_SERIAL_INIT`. Secondly you need to provide a function that writes the bytes somewhere,
and one that reads bytes if you use bidirectional communication.

```cpp
#include <metal/serial/core.h>
#include <stdio.h>


char metal_serial_read(); //implement!
void metal_serial_write(char c) { fputc(c, stdout);}; //implement

int main(int argc, char ** argv)
{    
    //This needs to be executed, AFTER metal_serial_read is ready to use 
    METAL_SERIAL_INIT();
    
    int res = do_something();

    //This macro tells the interpreter to exit.
    METAL_SERIAL_EXIT(res);
    return res;
}

```

In the above example you see, that the exit-code propagation is already built in. There is of course no need to put either call into the main-loop, 
you can embed it in your startup-code somwhere. 
 
## Generate

In order to run out program, we first need to generated the compile-database:

```bash
metal-serial-generate test.elf -S ./source -O test.db.json
```

The `test.elf` or `test.hex` combinded with the `test.db.json` are enough to get reproducible test runs.

If you write your own runner script, the internal function used is `metal.serial.generate`. 

## Interpret

The interpreter tool takes the database and binary input (and output with `-O` if you need this):

```bash
metal-serial-intepret -S test.db.json -I /dev/tty0
```

If you write your own runner script, the internal function used is `metal.serial.interpret`.

## MacroHooks

The extensibility of `metal.serial` is based on `MacroHook`s, which require a Macro and a call to `METAL_SERIAL_WRITE_LOCATION()`.

The exit-code-macro is implemented the following way:

```cpp
#define METAL_SERIAL_EXIT(Value) METAL_SERIAL_WRITE_MARKER(metal.exit); METAL_SERIAL_WRITE_INT(Value);
```

Now we can write a simple version of the macro hook like this:

```python
from metal.serial import MacroHook, MacroExpansion, Engine

class Exit(MacroHook):
    identifier = 'METAL_SERIAL_EXIT'
    
    def invoke(self, engine: Engine,  macro_expansion: MacroExpansion):
        self.exit_code = engine.read_int()
```

You can access the code through the `macro_expansion` while you need to explicitly invoke the read & write functions. The following are available:

| Target | Interpreter |
|--------|-------------|
| `METAL_SERIAL_WRITE_INT(Value)` | `engine.read_int() -> int` |
| `METAL_SERIAL_WRITE_MEMORY(Ptr, Size)` | `engine.read_memory() -> bytes` | 
| `METAL_SERIAL_WRITE_STR(Str)` | `engine.read_string() -> str` |
| `METAL_SERIAL_READ_INT(Value)` | `engine.write_int(int)` |
| `METAL_SERIAL_READ_MEMORY(Buffer, Size, ActuallyRead)` | `engine.write_memory(bytes) -> int` | 
| `METAL_SERIAL_READ_STR(Buffer, Size)` | `engine.write_string(str) -> int` |