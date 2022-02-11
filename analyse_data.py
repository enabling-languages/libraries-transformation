#!/usr/bin/env python3

# analyse_data.py
# 
#   Version 0.4.1
#   Copyright 2022 Enabling Languages.
#   Released under MIT license.

import os, sys, argparse
libpath = os.path.expanduser('./')
if libpath not in sys.path:
    sys.path.append(libpath)
import el_utils as elu
import pandas as pd
# import xlsxwriter

from pymarc import MARCReader
# from pymarc import exceptions as exc


def main():

    # Command line arguments
    parser = argparse.ArgumentParser(description='Blah blah blah')
    # Input file (Binary MARC file *.mrc) to be converted
    parser.add_argument('-i', '--input', type=str, required=True, help='Input file')
    # Debug mode
    parser.add_argument('-d', '--debug', action="store_true", required=False, help='Debug MARC records')
    # Parse the argument
    args = parser.parse_args()

    # Process CLI arguments
    # debug = False
    # if args.debug:
    #     debug = True
    debug = True if args.debug else False
    in_file = os.path.abspath(args.input)
    filename, file_extension = os.path.splitext(in_file)

    out_file = filename + ".xlsx"
    bib_data = []
    no_880_data = []
    bib_count = 0
    no_880 = 0

    with open(in_file, 'rb') as fh:
        reader = MARCReader(fh, to_unicode=True)
        for record in reader:
            bib_count += 1
            linkage = []
            field_list = []
            linkage_dict = {}
            if record['880'] is not None:
                for f in record.get_fields('880'):
                    field, pair = f['6'].split("-")
                    link = "880-" + pair
                    linkage.append(link)
                    field_list.append(field)
            else:
                no_880 += 1
                no_880_data.append(record['001'].value())
                print("No 880 fields: ", record['001'].value())
            field_list = list(set(field_list))
            for i in field_list:
                for j in record.get_fields(i):
                    linkage_dict[j['6']] = j.value()[7:]
            for f in record.get_fields('880'):
                    field, pair = f['6'].split("-")
                    match_pair = "880-" + pair
                    bib_id = record['001'].value()
                    try:
                        romanised_entry = linkage_dict[match_pair]
                    except KeyError:
                        print("Key error (linkage): ", bib_id, f['6'], match_pair)
                        romanised_entry = ""
                    lao_entry = f.value()[7:]
                    f_list = [bib_id, field, romanised_entry, lao_entry]
                    bib_data.append(f_list)

    if debug:
        if no_880 != 0:
            print("Number of records with no 880 field: ", no_880)
            print("BibIDs with no 880 field: " + ", ".join(no_880_data))
        print("Number of bib records: ", bib_count)

    source_df = pd.DataFrame(bib_data, columns = ['bibid', 'field', 'latin', 'lao'])
    df = source_df.copy()

    df['latin'] = df['latin'].str.normalize('NFD').str.replace("\u0327", "\u0328", regex=False).str.replace("\u031C", "\u0328", regex=False)
    df['lao'] = df['lao'].str.normalize('NFD')
    df_seg = df.copy()
    df['transliterated'] = df['latin'].map(lambda x: elu.el_transliterate(x, lang="lo", dir="reverse", nf="nfd"))
    df_seg['icu'] = df_seg['lao'].map(lambda x: elu.segment_words(x, engine="icu", lang="lo"))
    df_seg['laonlp'] = df_seg['lao'].map(lambda x: elu.segment_words(x, engine="laonlp", lang="lo"))

    unique_bibs = df['bibid'].nunique()
    if debug:
        print(f"Number of bibids in dataframe: {unique_bibs}")
        print(df['bibid'].value_counts())

    with pd.ExcelWriter(out_file) as writer:
        df.to_excel(writer, sheet_name='transliteration', index=False)
        df_seg.to_excel(writer, sheet_name='word segmentation', index=False)

    pickle_file = filename + ".pkl"
    pickle_sef_file = filename + "_seg.pkl"
    feather_file = filename + ".ftr"
    feather_seg_file = filename + "_seg.ftr"
    df.to_pickle(pickle_file)
    df_seg.to_pickle(pickle_sef_file)
    df.to_feather(feather_file)
    df_seg.to_feather(feather_seg_file)

    if bib_count == 1:
        print("Finished processing one record.")
    else:
        print(f"Finished processing {bib_count} records")
        if bib_count == 1:
            print(f"Datafram contains data from {unique_bibs} record")
        else:
            print(f"Dataframe contains data from {unique_bibs} records")

if __name__ == '__main__':
    main()

# ./analyse_data.py -i data/bibdata/set_a/set_a.mrc
# ./analyse_data.py -i data/bibdata/set_b/set_b.mrc