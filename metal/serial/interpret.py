import argparse
import json
import sys

from metal.serial import Engine
from metal.serial.generate import SerialInfo

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-S', '--serial-info',  required=True, help='The serial information perviously generated')
    parser.add_argument('-I', '--input',  help="The file for input data, defaults to stdin")
    parser.add_argument('-O', '--output', help="The output ,defaults to null.")

    args = parser.parse_args()

    serial_info = SerialInfo.from_dict(json.load(open(args.serial_info)))

    engine = Engine(input=open(args.input, 'rb') if args.input else sys.stdin,
                    output=open(args.output, 'wb') if args.output else None, serial_info=serial_info)

if __name__ == '__main__':
    main()