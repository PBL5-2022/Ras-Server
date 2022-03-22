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

    parser.add_argument('num',
                        type=str,
                        help='Device number')

    parser.add_argument('--onled', action='store_true',
                        help='Turn On Led')

    parser.add_argument('--offled', action='store_true',
                        help='Turn Off Led')
    
    parser.add_argument('--onmotor', action='store_true',
                        help='Turn On Motor')
    
    parser.add_argument('--offmotor', action='store_true',
                        help='Turn Off Motor')

    parser.add_argument('-o', '--only', action='store_true',
                        help='Count the lines of the files')

    options = parser.parse_args()
    num = int(options.num)

    if options.onled:
        l.turnOn(num,False)
    if options.offled:
        l.turnOff(num,False)

    if options.only:
        pprint("")


if __name__ == "__main__":
    main()
