# metal.gdb

*Study of the [Python API](https://sourceware.org/gdb/onlinedocs/gdb/Python-API.html) is highly recommended. 
Note that this repository contains a [pyi file](../gdb.pyi) for this api, though versios might differ.*

## metal.Breakpoint

Using the `gdb.Breakpoint` class we can define a breakpoint with a function that gets called when the breakpoint gets hit. 
Typically, an embedded system has a function `_exit(int)` that gets called when the program exits. 
If we want to forward that to `gdb` we have to call `quit` with the exit-code. This is simple enough:

```python
import gdb

class ExitBreakpoint(gdb.Breakpoint):
    def __init__(self):
        gdb.Breakpoint.__init__(self, "_exit")

    def stop(self):
        frame = gdb.selected_frame()
        
        # Get all values in the current block that arge arguments
        args = [arg for arg in frame.block() if arg.is_argument]    
        
        # Get the value and turn it into a string
        exit_code = str(args[0].value(frame))

        gdb.execute('quit {}'.format(exit_code))

bp = ExitBreakpoint()
```

So that's simple enough, what would we need metal.gdb for? The issue is the amount of breakpoints - if we add a breakpoint for every single thing, 
we might hit a limit that common microcontrollers have. So instead we put (almost everything) into one breakpoint.

```cpp
#include <metal/gdb/core.hpp>

void other_exit(int exit_code)
{
    metal_break("exit", exit_code); 
}
```

`metal_break` is the function that contains the singular breakpoint. The `metal.gdb` tool will (on import) generate that breakpoint and you can then register
your own receivers. Metal.gdb will also take care of the frame selection.

```python
import gdb
import metal.gdb

class ExitBreakpoint(metal.gdb.Breakpoint):
    def __init__(self):
        metal.gdb.Breakpoint.__init__(self, "exit")

    def stop(self):
        frame = gdb.selected_frame()
        args = [arg for arg in frame.block() if arg.is_argument]    
        exit_code = str(args[0].value(frame))

        gdb.execute('quit {}'.format(exit_code))

bp = ExitBreakpoint()
```

The `stop` function can get the `gdb.Breakpoint` object passed as it's first paramter. Furthermore you can use both at the sametime, like this:

```python 
class ExitBreakpoint(gdb.Breakpoint, MetalBreakpoint):
    def __init__(self):
        gdb.Breakpoint.__init__(self, "_exit")
        MetalBreakpoint.__init__(self, 'exit')

    def stop(self, bp=None):
        # handle to the gdb.Breakpoint 
        gdb_breakpoint = bp if bp else self    

bp = ExitBreakpoint()

```

The `exit-code` is provided as `metal.gdb.ExitBreakpoint` and gets setup when importing `metal.gdb.default`.

## Using plugins 

You can use python plugins in two ways in gdb:

```gdb
# Execute python directly
py print('hello world')

source hello_world.py
```

If you want to use metal.test with it's default settings, you just need to add:

```gdb
py import metal.gdb.default
#run the program
run
```

To make it completely automated, you put this into a command file, e.g. `test.gdbinit` and set it at launch:

```bash
gdb my_executable --init-command test.gdbinit
```

## Parameters

Configuration of provided plugins is provided through utilization of [`gdb.Paramter`](https://sourceware.org/gdb/onlinedocs/gdb/Parameters-In-Python.html#Parameters-In-Python)

```python
import gdb

class MyParameter(gdb.Parameter):
    def __init__(self):
        super(MyParameter, self).__init__("my-parameter", gdb.COMMAND_DATA, gdb.PARAM_UINTEGER)


myParamter = MyParameter()
```

In the `gdbinit` you can then set the value:

```gdbinit
set my-paramter 42
```


## Timeout 

An additional plugin provided by importing `metal.gdb.timeout` is the timeout. You can use it by setting the parameter `metal-timeout` to a value of seconds:

```gdb
set metal-timeout 60
``` 