#!/usr/bin/awk -f

# name:    best_conformer.awk
# author:  nbehrnd@yahoo.com
# license: GPL v2, 2022.
# date:    2022-03-17 (YYYY-MM-DD)
# edit:    2022-03-18 (YYYY-MM-DD)

# For each molecule DW suggested, report the conformer of lowest energy.
#
# Export a set of conformers by DataWarrior (hereafter DW) as a text file
# into a directory equally containing a copy of this AWK script.  The
# assumed layout of the tabulator separated data table written by DW is
#
# $1    the structure ID code (includes the conformation of the molecule)
# $2    the molecule ID (one molecule ID may match multiple conformers)
# $4    the energy attributed to the specific conformation $1 of $2
#
# i.e, the typical pattern if permutation of the stereogenic centers is
# disabled (the default suggested by DataWarrior).
#
# The script is to be used e.g., in the pattern of
#
# awk -f best_conformer.awk records_in.txt > conformers_out.dwar
#
# With file extension .dwar, the new record may be accessed directly by
# DataWarrior.  Alternatively, copy-paste the content (Edit -> Paste
# Special -> New From Data With Header Row) of the new record into a
# pristine session of DataWarrior.

BEGIN {
    FS = "\t";
    array[placeholder] = "dummy";
}

{if (NR == 1){
    print;
    }

if (NR >= 2) {
    key = $2;
    energy = $4;

    if (array[key] not in array) {array[key] = $0; counter++;} else {
        existing_array_entry = array[key];

        split(existing_array_entry, assistant_array);
        existing_array_energy = assistant_array[4];

        if (energy < existing_array_energy) {array[key] = $0}
        };
    }
}

END {
    delete array[placeholder];
    for (i = 1; i <= counter; i++){
        print array[i]
        };
    exit;
}
