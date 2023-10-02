# -*- coding: utf-8 -*-
# @Author: Sadamori Kojaku
# @Date:   2023-09-21 18:27:36
# @Last Modified by:   Sadamori Kojaku
# @Last Modified time: 2023-09-21 22:23:03
from scipy import stats
import numpy as np
import pandas as pd
import sys

if __name__ == "__main__":
    input_file = sys.argv[1]
    test_file = sys.argv[2]
    index_key = sys.argv[3]
    eval_key = sys.argv[4]
    criterion = sys.argv[5]

    df = pd.read_csv(input_file).rename(columns={eval_key: eval_key + "_input"})
    dg = pd.read_csv(test_file).rename(columns={eval_key: eval_key + "_test"})

    if not np.all(np.unique(df[index_key].values) == np.unique(dg[index_key].values)):
        raise ValueError(
            f"Some of {index_key} in your answer are missing or duplicated!"
        )

    dh = pd.merge(df, dg, on=index_key)

    if criterion == "equal":
        if not (np.all(dh[eval_key + "_input"] == dh[eval_key + "_test"])):
            raise ValueError(f"{eval_key} does not match.")
    elif criterion == "isclose":
        if not np.all(np.isclose(dh[eval_key + "_input"], dh[eval_key + "_test"])):
            raise ValueError(f"{eval_key} does not match.")
    elif criterion == "correlation":
        if not (
            stats.pearsonr(dh[eval_key + "_input"], dh[eval_key + "_test"])[0] >= 0.95
        ):
            raise ValueError(f"{eval_key} does not match.")

    print("Succesful!!💫")
