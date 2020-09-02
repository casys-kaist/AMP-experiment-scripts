#!/usr/bin/env python3

"""
   plot_normalized_performance_heatmap.py

    Created on: Jan. 07, 2020
        Author: Taekyung Heo <tkheo@casys.kaist.ac.kr>
"""

import argparse
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib import cm
mpl.use("Agg")
mpl.rcParams["legend.fancybox"] = False
mpl.rcParams["legend.edgecolor"] = "inherit"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-data", required=True)
    parser.add_argument("-result_dir", required=True)
    args = parser.parse_args()

    workload_name_df_dict = {}
    with open(args.data) as f:
        for line in f:
            splitted_line = line.strip().split(",")
            workload_name = splitted_line[0]
            act_scan_ratio = int(splitted_line[1])
            inact_scan_ratio = int(splitted_line[2])
            performance = float(splitted_line[3])
            if workload_name not in workload_name_df_dict.keys():
                df = {"Act Scan Ratio": [], "Inact Scan Ratio": [], "Performance": []}
                workload_name_df_dict.update({workload_name: df})
            df["Act Scan Ratio"].append(act_scan_ratio)
            df["Inact Scan Ratio"].append(inact_scan_ratio)
            df["Performance"].append(performance)

    for workload_name in workload_name_df_dict.keys():
        df = pd.DataFrame(workload_name_df_dict[workload_name])
        df = df.pivot("Act Scan Ratio", "Inact Scan Ratio", "Performance")
        df = df.transpose()
        workload_name_df_dict[workload_name] = df

    for workload_name in workload_name_df_dict.keys():
        df = workload_name_df_dict[workload_name]
        fig, ax = plt.subplots(figsize=(10, 10))
        sns.set(font_scale=3.5)
        sns.heatmap(df, ax=ax, cmap=cm.get_cmap("viridis_r"), annot=True, fmt=".0f", cbar=False)
        ax.invert_yaxis()
        ax.set_xticklabels(ax.get_xmajorticklabels(), fontsize=42)
        ax.set_yticklabels(ax.get_ymajorticklabels(), fontsize=42)
        ax.set_xlabel("Act Scan Ratio", fontsize=42)
        ax.set_ylabel("Inact Scan Ratio", fontsize=42)

        workload_name = workload_name.replace(" ", "_").replace(".", "_").replace("__", "_")
        plot_path = "%s/modified_lru_lists_performance_heatmap_%s" % (args.result_dir, workload_name)
        fig.savefig(plot_path + ".png", bbox_inches="tight")
        fig.savefig(plot_path + ".pdf", bbox_inches="tight")

if __name__ == "__main__":
    main()
