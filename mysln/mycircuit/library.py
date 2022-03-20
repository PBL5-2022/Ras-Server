import argparse
import pathlib
import pathlib
from pprint import pprint
from led import Led
import os


def main():
    l = Led()
    prog = 'python -m mylib.tool'
    description = ('A simple command line interface')

    parser = argparse.ArgumentParser(prog=prog, description=description)

    parser.add_argument('lednum',
                        type=str,
                        help='Led number')

    parser.add_argument('--turnonled', action='store_true',
                        help='Turn On Led')

    parser.add_argument('--turnoffled', action='store_true',
                        help='Turn Off Led')

    parser.add_argument('-o', '--only', action='store_true',
                        help='Count the lines of the files')

    options = parser.parse_args()
    lednum = int(options.lednum)

    if options.turnonled:
        l.turnOn(lednum,False)
    if options.turnoffled:
        l.turnOff(lednum,False)

    if options.only:
        pprint("")


if __name__ == "__main__":
    main()
