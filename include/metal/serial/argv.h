#ifndef METAL_TEST_SERIAL_ARGV_H
#define METAL_TEST_SERIAL_ARGV_H

#include <metal/serial/core.h>

#define METAL_SERIAL_INIT_ARGV() METAL_SERIAL_WRITE_LOCATION();


static int metal_serial_init_argv(int * argc, char **argv[], void * buf, int sz)
{
    METAL_SERIAL_INIT_ARGV();

    int argc_ = 0;
    METAL_SERIAL_READ_INT(argc_);

    char **argv_ = (char **)buf;
    argv_ += argc_;
    char * content = (char*)(argv_ + argc_);

    int actually_read = 0;
    int buffer_size = sz - (argc_ * sizeof(char*));
    METAL_SERIAL_READ_MEMORY(content, buffer_size, actually_read);

    char * end = content + actually_read;

    int i = 0;
    for (; (i<argc_) && (content < end); i++)
    {
        //check if the current string is completely in the buffer
        char * start = content;
        while ((*content != '\0') && (content < end))

            content++;

        content += 1;

        if (content > end)
            break;

        argv_[i] = start;
    }

    *argc = i;
    *argv = argv_;
    return (buffer_size == actually_read);
}

#undef METAL_SERIAL_INIT_ARGV

#endif //METAL_TEST_SERIAL_ARGV_H
