#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# name   : best_conformer.py
# author : nbehrnd@yahoo.com
# license: GPLv2
# date   : [2023-06-07 Wed]
# edit   : [2025-01-30 Thu]
"""
report the conformer (by ID and stereo label) of lowest energy to the CLI

For a given (set) of structure(s), DataWarrior can generate conformers, an
iteration which may interconvert the (RS) configuration of the molecules in
question.  To retain a recognizable relationship, the corresponding enantiomers
and diastereomers then (still) carry the same structure ID, but differ by the
stereo tag -- both values are an integer.  Once exported as a .txt file, this
script reports for each isomer the conformer of lowest energy to the CLI, e.g.

```shell
python best_conformer.py conformers.txt
```

a result which can be redirected into a permanent record (`>`).  For ease of
portability, this implementation only depends on Python's standard library."""

import argparse
import re


def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description="report the lowest energy conformer per ID isomer to the CLI",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "file",
        help="DataWarrior's conformer list, exported as .txt file",
        type=argparse.FileType("rt"),
        default=None,
    )

    return parser.parse_args()


def identify_column_headers(raw_data):
    """check columns' ID, Stereo Isomer, and Energy position"""
    with open(raw_data, mode="rt", encoding="utf-8") as source:
        table_header = source.readline().strip()

    column_heads = table_header.split("\t")
    # for the structure ID (though enantiomers, diastereomers share an ID here)
    list_of_matches = [
        i for i, item in enumerate(column_heads) if re.search("ID", item)
    ]
    column_id = int(list_of_matches[0])

    # for the stereo ID
    list_of_matches = [
        i for i, item in enumerate(column_heads) if re.search("Stereo Isomer", item)
    ]
    column_stereo = int(list_of_matches[0])

    # for the energy of the present conformer
    list_of_matches = [
        i for i, item in enumerate(column_heads) if re.search("Energy", item)
    ]
    column_energy = int(list_of_matches[0])

    return column_heads, column_id, column_stereo, column_energy


def process_dw_txt(raw_data, column_id, column_stereo, column_energy):
    """identify the lowest energy isomer conformers

    Because DataWarrior can interconvert RS configurations, both the (parental)
    ID as well as the stereo chemical counter for this ID enter as key for the
    dictionary approach.  Simple concatenation of the strings could introduce
    ambiguity here, hence the underscore as a distinct separator between the
    two integers.
    It then is a question to check if the key is known to the dictionary, and
    if so, to decide by comparison of the energies if the current entry from
    DataWarrior's file is to replace the entry in the intermediate dictionary,
    or not."""
    report_dictionary = {}

    with open(file=raw_data, mode="rt", encoding="utf-8") as source:
        for linenumber, line in enumerate(source):
            if linenumber > 0:  # because the headline is irrelevant here
                entry = str(line).strip().split("\t")
                key = "_".join([entry[column_id], entry[column_stereo]])

                if key not in report_dictionary:
                    report_dictionary[key] = "\t".join(entry)

                elif key in report_dictionary:
                    energy_from_dictionary = float(
                        report_dictionary.get(key).split("\t")[column_energy]
                    )

                    energy_from_list = float(entry[column_energy])

                    if energy_from_list < energy_from_dictionary:
                        report_dictionary[key] = "\t".join(entry)

    return report_dictionary


def report_results(headline, dictionary):
    """report the lowest energy conformers per isomer

    The keys do not enter the report, nor is a need for a key based sort.  Thus
    a report of the dictionary's values appears as good enough."""
    listing = []
    listing = list(dictionary.values())

    headline = "\t".join(headline)
    print(f"{headline}\n")

    for entry in listing:
        print(entry)


def main():
    """Join the functionalities"""

    args = get_args()

    column_heads, column_id, column_stereo, column_energy = identify_column_headers(
        args.file.name
    )
    query_data = process_dw_txt(args.file.name, column_id, column_stereo, column_energy)
    report_results(column_heads, query_data)


# --------------------------------------------------
if __name__ == "__main__":
    main()
