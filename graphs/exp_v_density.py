#!/user/bin/env/python3

"""

"""

__author__ = "Scott Teresi"

import argparse
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from expression.import_expression import import_exp_dataframe


def exp_vs_density(
    density_vals, exp_matrix, matrix_type, window, te_type, direction, output_dir
):
    """
    Upstream or Downstream:
        X-Axis: Density in a specific window from 0 to 1
        Y-Axis: Gene expression (TPM)

    Args:
        exp_matrix (pandas.core.frame.DataFrame): Pandas dataframe representing
            either fpkm or tpm, shape: (genes, libraries)
        matrix_type (str): FPKM or TPM
        window (int): Integer representing the window for the analysis
        te_type (str): String of the TE name for the analysis
        direction (str): Upstream or downstream
        output_dir (str): Path representing folder to save to

    """
    # TODO
    # Raise ValueError if direction does not fit within the categories.
    # plt.scatter(density_vals, exp_matrix)
    # plt.title(
    # os.path.join(output_dir, (str(window) + str(te_type) + "_Density_vs_Exp.png"))
    # )
    # plt.xlabel("Transposon Density")
    # NOTE are we using log base 2?
    # plt.ylabel("Gene Expression (Log(2) TPM")
    # plt.show()

    # exp_matrix = np.around(exp_matrix, 2)
    # density_vals = np.around(density_vals, 2)
    # sns.relplot(x=density_vals, y=exp_matrix, kind="line")
    # plt.show()
    # data = exp_matrix


def import_old_density(filename):
    data = pd.read_csv(filename, header="infer", sep=",", index_col="maker_name")
    data = data[["LTR_left"]]
    return data


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    path_main = os.path.abspath(__file__)

    parser.add_argument("fpkm_data", type=str, help="parent path of FPKM matrix")
    parser.add_argument("tpm_data", type=str, help="parent path of TPM matrix")
    parser.add_argument("test_density_data", type=str, help="old density data")
    parser.add_argument(
        "--output_dir",
        type=str,
        help="path to output folder",
        default=os.path.join(path_main, "../../", "TE_Data/graphs/"),
    )

    args = parser.parse_args()
    args.fpkm_data = os.path.abspath(args.fpkm_data)
    args.tpm_data = os.path.abspath(args.tpm_data)
    args.test_density_data = os.path.abspath(args.test_density_data)
    args.output_dir = os.path.abspath(args.output_dir)

    fpkm_data = import_exp_dataframe(args.fpkm_data)
    tpm_data = import_exp_dataframe(args.tpm_data)
    old_density = import_old_density(args.test_density_data)
    old_density = old_density / 2  # this step is done because the old density
    # data needs to be corrected

    merged = old_density.join(tpm_data)  # this step is necessary because we
    # don't have all the genes yet in the denisty data. It is easy to work with
    # a dataframe in which all of the expression values and density values are
    # together.  However I am not sure how this will work with the hdf5 format.

    merged["Exp_Fruit"] = tpm_data[
        ["ERR855501", "ERR855502", "ERR855503", "ERR855504", "ERR855505"]
    ].mean(axis=1)

    merged = merged[merged.Exp_Fruit != 0]  # remove exp vals with zero
    merged["Exp_Fruit"] = np.log2(merged["Exp_Fruit"])
    sns.jointplot(x="LTR_left", y="Exp_Fruit", data=merged, kind="reg")

    plt.show()