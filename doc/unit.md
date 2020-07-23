# Unit test library

 * two test levels (assertion/expectation)
 * flow control (cancel tests/critical tests)
 * log messages
 * test cases
 * human-readable-format or json output
 * success indication through the exit-code
 * C and C++ implementation

Here's a simple example of a test with `metal.unit`:

```cpp
#include <metal/gdb/unit.hpp>

int main(int argc, char *argv[])
{
    int i = 41;
    i++;

    METAL_ASSERT(i == 42);
    return METAL_REPORT();
}
```

With metal.unit you need to select one of the following backends or provide your own by defining `METAL_TEST_REPORT`:

| Backend | Include |
|---------|---------|
| `metal.gdb` | `<metal/gdb/unit.hpp>` |
| `metal.serial` | `<metal/serial/unit.hpp>` |
| hosted | `<metal/hosted/unit.hpp>` |

`hosted` will just generate formatted output (with printf) and return 1 on error.

**Only gdb will output the actual values of the tests, while serial & hosted only output the condition.**


## Test Levels and Macros

`metal.unit` provides two test levels, `error` and `warning` expressed in the code as

  * `ASSERT`
  * `EXPECT`

Both will be written into the console, but only errors will cause the test to fail, i.e. return a value != 0, that is.

The plain assertions are 

  * `METAL_ASSERT(Condition)` 
  * `METAL_EXPECT(Condition)` 

Then there are two utility macros for logging the current position with or without a custom message. 
    
    * `METAL_LOG(Message)`
    * `METAL_CHECKPOINT()`


All other tests are implemented through macros, so parameter names and location can be obtained easily. That way the backend can provide 
detailed information of the code. The usual format for the macros looks like this:

```
    METAL_``['`level`]``_``['test-name]``(``['arguments]``);
```

Using C++ will enable decomposition, which means that you probably only need the plain asserts.

** Note that GDB will most likely evaluate your expressions for the following macros twice - so if you use a function in the macro it will be invoked twice.**

Here's a list of test types:

| Macro | Description |
|-------|-------------| 
| `MESSAGE(Condition, Message)` | Plain assertion, but custom message. |
| `EQUAL(Lhs, Rhs)` | Equality check |
| `NOT_EQUAL(Lhs, Rhs)` | Inequalit check |
| `GE(Lhs, Rhs)` | Greater or equal |
| `LE(Lhs, Rhs)` | Lesser or equal |
| `GREATER(Lhs, Rhs)` | Greater | 
| `LESSER(Lhs, Rhs)`  | Lesser | 
| `PREDICATE(Function, Args...)` | Check that calling `Function(Args...)` yields true. |
| `CLOSE(Lhs, Rhs, Tolerance)` | Check that Lhs is withing Rhs +- Tolerance |
| `CLOSE_RELATIVE(Lhs, Rhs, Tolerance)` | Check that Lhs is withing Rhs +- Tolerance, where the tolerance is a fraction of Rhs. |



As an example, we use the equality check:

```cpp
METAL_ASSERT_EQUAL(x, y);
METAL_EXPECT_EQUAL(i, j);
```

For the given example, the output could look like this on gdb.

```
    test.cpp(10) assertion succeeded [equality]: x == y; [3 == 3]
    test.cpp(11) expectation failed [equality]: i == j; [42 == -1]
```

end like this when useing hosted or with serial:

```
    test.cpp(10) assertion succeeded [equality]: x == y
    test.cpp(11) expectation failed [equality]: i == j
```

## Decomposition (C++) 

Decomposition is a technique used by `catch2` based no expression templates, to detect and decompose expression, like `a == b`. When using C++ this 
is activated by default for `METAL_ASSERT` and `METAL_EXPECT`. You will however only see a difference on gdb, since serial & hosted don't output values.

```cpp
METAL_ASSERT(x == y);
METAL_EXPECT(i == j);
```

Given the above example using composition

```
    test.cpp(10) assertion succeeded [equality]: x == y; [3 == 3]
    test.cpp(11) expectation failed [equality]: i == j; [42 == -1]
```

yet on hosted or serial, it will be this:

```
    test.cpp(10) assertion succeeded [plain]: x == y
    test.cpp(11) expectation failed [plain]: i == j
```

In addition to the binary expressions, we also support the close comparisions, with the following syntax:

```cpp
using metal::unit::operator""_eps; //or just use metal::unit::epsilon directly... 

METAL_ASSERT(x == y +-   10_eps); //same as METAL_ASSERT_CLOSE
METAL_ASSERT(x == y +- ~0.1_eps); //same as METAL_ASSERT_CLOSE_RELATIVE
```

## Test Cases

You can use `METAL_CALL` to manually register (and nest) test cases:

```cpp

void test_case_1() {}
void test_case_2() {}

int main(int argc, char * argv[])
{
    METAL_CALL(test_case_1);
    METAL_CALL(test_case_2, "Some description");
    return METAL_ERROR();
}
```

Alternatively you can use the `METAL_CASE` macro to automatically register tests. You can then either invoke `metal_unit_test_case_registry_run()` or 
`#define` `METAL_UNIT_MAIN` before including `serial` to take the default `main` function. The latter has the advantage of already including 
`METAL_SERIAL_INIT` and `METAL_SERIAL_EXIT` calls when used with `metal.serial`.

```cpp
#define METAL_UNIT_MAIN

#include <metal/serial/unit.hpp>

TEST_CASE(" test case 1")
{    
}

TEST_CASE("test case 2")
{    
}
```

## Flow control - critical & loops (GNUC only)

*This part utilizes [labels as values](https://gcc.gnu.org/onlinedocs/gcc/Labels-as-Values.html) and is thus only available on gcc and clang.*

### Critical

metal.unit lets you define critical sections or statements. That is, if an assertion or expectation fails it aborts. Aborting is done through returning, 
so you can provide a return value if your function shall have one.  
    
```cpp

int my_sub_test(int x, int y)
{    
    METAL_CRITICAL(METAL_ASSERT_GE(x,y), -1); //cancel with -1 if it fails
}

void other_sub_test(int x)
{
    METAL_CRITICAL(METAL_ASSERT_GE(x,0)); //cancel if it fails    
}

int next_sub_test(int x, int y)
{    
    { //strict C89, any of the following will cause a return with -1 -> can be omitted for void
        METAL_ENTER_CRITICAL_SECTION(-1);
        METAL_ASSERT_GE(x, 0);
        METAL_EXPECT_GE(y, x);
    }
}

void last_sub_test(int x, int y) 
{
    //C99 and C++
    METAL_CRTICAL_SECTION(/* return value goes here */)
    {
    
        METAL_ASSERT_GE(x, 0);
        METAL_EXPECT_GE(y, x);
    }
}
```

### For loops (C99 and C++)

metal.unit also provides a way to declare a for loop, that breaks once an error occurs:

```cpp
METAL_FOR(int i = 0; i< 10;  i++)
    METAL_ASSERT_LE(i , 3); //breaks when i == 4
```

## Ranged operations

`METAL_RANGED` makes working with containers easier. It takes two (indexible) ranges by object & length and will invoke the macro with every pair. You can
pass more parameter, e.g. if you want to use a `CLOSE` macro. Just like the for loop, the range will break once an assertion or expectation fails.

```cpp
int arr[4] = {1,2,3,4};
double vals[4] = {1.1, 2.2, 3.3, 4.4};

METAL_RANGED(arr, 4, vals, 4, METAL_ASSERT_LE); //passes
METAL_RANGED(arr, 4, vals, 4, METAL_ASSERT_CLOSE_RELATIVE, 0.11); //passes 
```

Since this is just a macro expansion, you can also provide your own macro or function .that combines several assertions

## METAL_REPORT

The METAL_REPORT() macro triggers printing of the final results. 