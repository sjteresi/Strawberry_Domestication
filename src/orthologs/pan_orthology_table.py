#!/usr/bin/env python3

__author__ = "Scott Teresi"

import pandas as pd
import numpy as np

import os
import argparse
import logging
import coloredlogs

from src.orthologs.syntelogs import read_cleaned_syntelogs
from src.orthologs.homologs import read_cleaned_homologs

"""
- TODO
"""


def DN_RR_merge_homologs_and_syntelogs(homologs, syntelogs):
    """
    Merge the homolog and syntelog dataframes
    """

    # Sort the syntelogs in alphabetical order by Royal Royce gene name
    syntelogs.sort_values(by=["RR_Gene"], inplace=True)

    # Are there any Royal Royce syntelogs that are not unique?
    # Yes indeed there are quite a lot...
    # print(syntelogs.loc[syntelogs.duplicated(subset=["RR_Gene"], keep=False)])

    # Let's merge the homologs and syntelogs
    # First I will rename the columns in the homolog file to make it easier to
    # merge
    homologs.rename(
        columns={
            "Del_Norte": "DN_Gene",
            "Royal_Royce": "RR_Gene",
            "E_Value": "BLAST_E_Value",
        },
        inplace=True,
    )
    # I will also rename the E_Value column in the syntelog file
    syntelogs.rename(columns={"E_Value": "Syntelog_E_Value"}, inplace=True)

    # Now I will merge the two dataframes
    merged_all = pd.concat([homologs, syntelogs], axis=0, join="outer")

    # Sort the merged dataframe by Royal Royce gene name and Point_of_Origin,
    # then by Evalues
    merged_all.sort_values(
        by=["RR_Gene", "Point_of_Origin", "Syntelog_E_Value", "BLAST_E_Value"],
        ascending=[True, False, True, True],
        inplace=True,
    )

    return merged_all


def H4_RR_merge_homologs_and_syntelogs(homologs, syntelogs):
    """
    Merge the homolog and syntelog dataframes
    """

    # Sort the syntelogs in alphabetical order by Royal Royce gene name
    syntelogs.sort_values(by=["RR_Gene"], inplace=True)

    # Are there any Royal Royce syntelogs that are not unique?
    # Yes indeed there are quite a lot...
    # print(syntelogs.loc[syntelogs.duplicated(subset=["RR_Gene"], keep=False)])

    # Let's merge the homologs and syntelogs
    # First I will rename the columns in the homolog file to make it easier to
    # merge
    homologs.rename(
        columns={
            "H4": "H4_Gene",
            "Royal_Royce": "RR_Gene",
            "E_Value": "BLAST_E_Value",
        },
        inplace=True,
    )
    # I will also rename the E_Value column in the syntelog file
    syntelogs.rename(columns={"E_Value": "Syntelog_E_Value"}, inplace=True)

    # Now I will merge the two dataframes
    merged_all = pd.concat([homologs, syntelogs], axis=0, join="outer")

    # Convert the H4 chromosome column to string
    merged_all["H4_Chromosome"] = merged_all["H4_Chromosome"].astype(str)

    # Sort the merged dataframe by Royal Royce gene name and Point_of_Origin,
    # then by Evalues
    merged_all.sort_values(
        by=["RR_Gene", "Point_of_Origin", "Syntelog_E_Value", "BLAST_E_Value"],
        ascending=[True, False, True, True],
        inplace=True,
    )

    return merged_all


if __name__ == "__main__":

    path_main = os.path.abspath(__file__)
    dir_main = os.path.dirname(path_main)
    parser = argparse.ArgumentParser(description="TODO")

    parser.add_argument("H4_RR_cleaned_syntelog_input_file", type=str, help="TODO")
    parser.add_argument("H4_RR_cleaned_homolog_input_file", type=str, help="TODO")
    parser.add_argument("DN_RR_cleaned_syntelog_input_file", type=str, help="TODO")
    parser.add_argument("DN_RR_cleaned_homolog_input_file", type=str, help="TODO")
    parser.add_argument(
        "output_dir",
        type=str,
        help="Path and filename to output results",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="set debugging level to DEBUG"
    )

    args = parser.parse_args()

    # H4 files
    args.H4_RR_cleaned_syntelog_input_file = os.path.abspath(
        args.H4_RR_cleaned_syntelog_input_file
    )
    args.H4_RR_cleaned_homolog_input_file = os.path.abspath(
        args.H4_RR_cleaned_homolog_input_file
    )

    # DN files
    args.DN_RR_cleaned_syntelog_input_file = os.path.abspath(
        args.DN_RR_cleaned_syntelog_input_file
    )
    args.DN_RR_cleaned_homolog_input_file = os.path.abspath(
        args.DN_RR_cleaned_homolog_input_file
    )

    args.output_dir = os.path.abspath(args.output_dir)

    log_level = logging.DEBUG if args.verbose else logging.INFO
    logger = logging.getLogger(__name__)
    coloredlogs.install(level=log_level)

    # Begin work, read in the data
    H4_RR_syntelogs = read_cleaned_syntelogs(args.H4_RR_cleaned_syntelog_input_file)
    H4_RR_homologs = read_cleaned_homologs(args.H4_RR_cleaned_homolog_input_file)

    DN_RR_syntelogs = read_cleaned_syntelogs(args.DN_RR_cleaned_syntelog_input_file)
    DN_RR_homologs = read_cleaned_homologs(args.DN_RR_cleaned_homolog_input_file)

    H4_RR_orthologs = H4_RR_merge_homologs_and_syntelogs(
        H4_RR_homologs, H4_RR_syntelogs
    )
    DN_RR_orthologs = DN_RR_merge_homologs_and_syntelogs(
        DN_RR_homologs, DN_RR_syntelogs
    )

    output_file = os.path.abspath(os.path.join(args.output_dir, "DN_RR_orthologs.tsv"))
    logger.info(f"Writing DN-RR orthologs to {output_file}")
    DN_RR_orthologs.to_csv(output_file, sep="\t", index=False, header=True)

    output_file = os.path.abspath(os.path.join(args.output_dir, "H4_RR_orthologs.tsv"))
    logger.info(f"Writing H4-RR orthologs to {output_file}")
    H4_RR_orthologs.to_csv(output_file, sep="\t", index=False, header=True)

    # Ok at this point, both ortholog tables are in RAM. Now I need to merge
    # them as well.