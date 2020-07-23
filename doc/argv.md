# Argv

To avoid allocations, argv-propagation is based on a static buffer. That is, `metal.gdb` will try to find the buffer and call `malloc` if it is not available,
`metal.serial` will only work with a pre-allocated buffer.

# metal.serial

`metal.serial` provides the `metal.serial.Argv` class, which is not included in the defaults, since it requires writing to the target.

```python
from metal.serial import Engine, Exit
from metal.serial.argv import build_argv_hook
from metal.serial.generate import generate


input = open('/dev/tty0/', 'r') 
output = open('/dev/tty0/', 'w')

my_argv = ['--some-arg', '42']

serial_info = generate('my_binary.elf', [], [], ['METAL_SERIAL_INIT_ARGV'])
engine = Engine(input=input, output=output, serial_info=serial_info, macro_hooks=[Exit, build_argv_hook(my_argv))
``` 

On the target, you then need to call `metal_serial_init_argv` like this:


```cpp

#include <metal/serial/argv.h> 

char metal_serial_read(); //required
void metal_serial_write(char c); //required

int main(int argc, char * args[])
{
    METAL_SERIAL_INIT();

    char buf[100];

    metal_serial_init_argv(&argc, &args, buf, sizeof(buf));

    //do something

    METAL_SERIAL_EXIT(0);
    return 0;
}
```

You can of course put this in the startup code that call `main`.

# GDB

On gdb this is much simpler and active by default:

```cpp
int main(int argc, char *argv[])
{
    char argv_buffer[100];
    metal_break("argv", argc, argv);
    return 0;
}
```

`metal.gdb` will check if a variables called `argv_buffer` is available and call `sizeof` on it. If this doesn't work it will invoke `malloc` to allocate the buffer. 