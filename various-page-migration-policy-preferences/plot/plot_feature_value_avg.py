#!/usr/bin/env python3

"""
   plot_feature_value_avg.py

    Created on: Dec. 27, 2019
        Author: Taekyung Heo <tkheo@casys.kaist.ac.kr>
"""

import argparse
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import cm
from matplotlib.colors import ListedColormap
from common import *
mpl.use("Agg")
mpl.rcParams["legend.fancybox"] = False
mpl.rcParams["legend.edgecolor"] = "inherit"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-data", required=True)
    parser.add_argument("-result_dir", required=True)
    args = parser.parse_args()

    cmap_big = cm.get_cmap("viridis", 512)
    cmap_small = ListedColormap(cmap_big(np.linspace(0.0, 0.65, 256)))

    data = {}
    with open(args.data) as f:
        for line in f:
            splitted_line = line.strip().split(",")
            workload_name = splitted_line[0]
            thp = splitted_line[1]
            if thp == "always":
                mig_policy = splitted_line[2]
                feature_value = float(splitted_line[3])
                if workload_name not in data.keys():
                    data.update({workload_name:
                        {"LRU": 0,
                         "LFU": 0,
                         "Random": 0}})
                data[workload_name][mig_policy] = feature_value

    plot_data = {"Workload Name": abbr_workload_name_li, "LRU": [], "LFU": [], "Random": []}
    for abbr_workload_name in abbr_workload_name_li:
        plot_data["LRU"].append(data[abbr_workload_name]["LRU"])
        plot_data["LFU"].append(data[abbr_workload_name]["LFU"])
        plot_data["Random"].append(data[abbr_workload_name]["Random"])

    feature_name = args.data.split("/")[-1].replace(".txt", "").replace("_avg", "")
    print(" ".join(feature_name.split("_")).title(), "Avg")
    for key in ["LRU", "LFU", "Random"]:
        print(key, plot_data[key])
    print()

    df = pd.DataFrame(plot_data)
    ax = df.plot.bar(x="Workload Name",
            y=["LRU", "LFU", "Random"],
            rot=80, figsize=(13, 4),
            width=0.83, cmap=cmap_small)
    ax.tick_params(axis="x", labelsize=25.5)
    ax.tick_params(axis="y", labelsize=25.5)
    ax.xaxis.label.set_visible(False)
    ax.get_legend().remove()
    ax.grid(linestyle="--", alpha=0.8)
    ax.set_ylim([0, 100.000001])
    start, end = ax.get_ylim()
    ax.yaxis.set_ticks(np.arange(start, end, 20))

    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.2, box.width, box.height * 0.8])

    ax.legend(["LRU", "LFU", "Random"], loc="upper center",
            bbox_to_anchor=(0.48, -1.3), fontsize=25.5, ncol=4)
    ax.axvline(x=2.5, color='k', linestyle="--", linewidth=2)
    ax.axvline(x=6.5, color='k', linestyle="--", linewidth=2)
    ax.axvline(x=9.5, color='k', linestyle="--", linewidth=2)

    ax.text(0.2, 105, "LRU-favor", fontsize=23)
    ax.text(3.8, 105, "LFU-favor", fontsize=23)
    ax.text(6.76, 105, "Random-favor", fontsize=23)
    ax.text(9.42, 105, "Neutral", fontsize=23)

    if feature_name == "page_migration_stability":
        ax.set_ylabel("Page Migration Stability (%)", fontsize=25.5)
        ax.yaxis.set_label_coords(-0.08, 0.14)
    if feature_name == "accessed_pages_ratio":
        ax.set_ylabel("Accessed Page Ratio (%)", fontsize=25.5)
        ax.yaxis.set_label_coords(-0.08, 0.20)
    if feature_name == "fast_memory_hit_ratio":
        ax.set_ylabel("Fast Mem. Hit Ratio (%)", fontsize=25.5)
        ax.yaxis.set_label_coords(-0.08, 0.25)
    if feature_name == "fast_memory_access_ratio":
        ax.set_ylabel("Fast Mem. Access Ratio (%)", fontsize=25.5)
        ax.yaxis.set_label_coords(-0.08, 0.13)

    fig = ax.get_figure()
    plot_path = "%s/migration_policy_%s" % (args.result_dir, feature_name)
    fig.savefig(plot_path + ".png", bbox_inches="tight")
    fig.savefig(plot_path + ".pdf", bbox_inches="tight")
    plt.close()

if __name__ == "__main__":
    main()
