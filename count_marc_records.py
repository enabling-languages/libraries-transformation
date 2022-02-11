#!/usr/bin/env python3

# analyse_data.py
# 
#   Version 0.4.0
#   Copyright 2022 Enabling Languages.
#   Released under MIT license.

import os, sys, argparse
# libpath = os.path.expanduser('./')
# if libpath not in sys.path:
#     sys.path.append(libpath)
# import el_utils as elu
# import pandas as pd
# import xlsxwriter

from pymarc import MARCReader


def main():

    # Command line arguments
    parser = argparse.ArgumentParser(description='Blah blah blah')
    # Input file (Binary MARC file *.mrc) to be converted
    parser.add_argument('-i', '--input', type=str, required=True, help='Input file')
    # Parse the argument
    args = parser.parse_args()

    in_file = os.path.abspath(args.input)

    bib_data = []

    bib_count = 0

    #bib_count = sum (1 for rec in MARCReader(open(in_file))) 
   

    bib_count = 0
    for rec in MARCReader(open(in_file, "r")):
        bib_count += 1
    print(f"{bib_count} records in MARC file.")



if __name__ == '__main__':
    main()

# ./count_marc_records.py -i data/bibdata/set_a/set_a.mrc
# ./count_marc_records.py -i data/bibdata/set_b/set_b.mrc