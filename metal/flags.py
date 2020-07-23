import pathlib
import sys
import argparse

def print_flags():
    parser = argparse.ArgumentParser()

    parser.add_argument('-P', '--path',         help="Print the root path of the project",  action='store_true')
    parser.add_argument('-I', '--include-path', help="Print the include path for the compiler",  action='store_true')
    parser.add_argument('-S', '--source',       help="Source files for a backend", choices=['gdb', 'serial'])
    parser.add_argument('-N', '--newlib',       help='The defined for the different newlib modes available for serial', choices=['blocked', 'unchecked', 'full'])


    args = parser.parse_args()

    if args.path:
        sys.stdout.write(str(pathlib.Path(__file__).parent.parent.absolute()) + ' ')
    if args.include_path:
        sys.stdout.write('-I' + str(pathlib.Path(__file__).parent.parent.absolute() / 'include') + ' ')
    if args.source:
        sys.stdout.write(str(pathlib.Path(__file__).parent.parent.absolute() / 'src' / 'metal' / args.source / 'syscalls.c' ) + ' ')
    if args.newlib == 'blocked':
        sys.stdout.write('-DMETAL_SERIAL_SYSCALLS_MODE=METAL_SERIAL_SYSCALLS_MODE_BLOCKED ')
    elif args.newlib == 'unchecked':
        sys.stdout.write('-DMETAL_SERIAL_SYSCALLS_MODE=METAL_SERIAL_SYSCALLS_MODE_UNCHECKED ')
    elif args.newlib == 'full':
        sys.stdout.write('-DMETAL_SERIAL_SYSCALLS_MODE=METAL_SERIAL_SYSCALLS_MODE_FULL ')

if __name__ == "__main__":
    print_flags()