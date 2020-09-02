#!/usr/bin/env python3

"""
   plot_migration_policy_selections_stacked_bar.py

    Created on: Dec. 26, 2019
        Author: Taekyung Heo <tkheo@casys.kaist.ac.kr>
"""

import argparse
import matplotlib as mpl
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import cm
from matplotlib.colors import ListedColormap
from lib.stats import *
from common import *
mpl.use("Agg")
mpl.rcParams["legend.fancybox"] = False
mpl.rcParams["legend.edgecolor"] = "inherit"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-result_dir", required=True)
    parser.add_argument("-data", required=True)
    args = parser.parse_args()

    # load data
    data_dict = {}
    with open(args.data) as f:
        for line in f:
            splitted_line = line.strip().split(",")
            abbr_workload_name = splitted_line[0]
            mig_policy = int(splitted_line[1])
            selection_ratio = float(splitted_line[2])
            if abbr_workload_name not in data_dict.keys():
                data_dict.update({abbr_workload_name: {}})
            data_dict[abbr_workload_name].update({mig_policy: selection_ratio})

    # print selection ratios
    print()
    print("Selection Ratios")
    for abbr_workload_name in abbr_workload_name_li:
        print(abbr_workload_name, data_dict[abbr_workload_name])
    print()

    # prepare data_dict
    plot_data = [[], [], []]
    for abbr_workload_name in abbr_workload_name_li:
        plot_data[0].append(abbr_workload_name)
        plot_data[1].append("LRU")
        plot_data[2].append(data_dict[abbr_workload_name][MIG_POLICY_LRU])

        plot_data[0].append(abbr_workload_name)
        plot_data[1].append("LFU")
        plot_data[2].append(data_dict[abbr_workload_name][MIG_POLICY_LFU])

        plot_data[0].append(abbr_workload_name)
        plot_data[1].append("Random")
        plot_data[2].append(data_dict[abbr_workload_name][MIG_POLICY_PSEUDO_RANDOM])

    # plot stacked bar chart
    fig = plt.figure(figsize=(9.0, 1.8))
    gs = gridspec.GridSpec(1, 1)
    ax = plt.subplot(gs[0])

    # prepare colormap
    cmap_big = cm.get_cmap("viridis", 512)
    cmap_small = ListedColormap(cmap_big(np.linspace(0.0, 0.65, 256)))

    # plot
    rows = zip(plot_data[0], plot_data[1], plot_data[2])
    df = pd.DataFrame(rows, columns=["Workload Name", "Replacement Policy", "Ratio"])
    pivot_df = df.pivot(index="Workload Name", columns="Replacement Policy", values="Ratio")
    pivot_df = pivot_df.reindex(abbr_workload_name_li)
    pivot_df.loc[:,["Random", "LFU", "LRU"]].plot.bar(ax=ax, stacked=True, cmap=cmap_small)

    # set parameters
    ax.xaxis.label.set_visible(False)
    ax.set_ylabel("Selection Ratio (%)", fontsize=18)
    ax.yaxis.set_label_coords(-0.09, 0.25)
    ax.set_xticklabels(pivot_df.index, rotation=70)
    ax.tick_params(axis="x", labelsize=17)
    ax.tick_params(axis="y", labelsize=17)
    ax.set_ylim((0, 100.00001))
    start, end = ax.get_ylim()
    ax.yaxis.set_ticks(np.arange(start, end, 25))
    ax.grid(linestyle="--", alpha=0.8)

    # add legend
    h, l = ax.get_legend_handles_labels()
    h = list(reversed(h))
    l = list(reversed(l))
    l1 = ax.legend(h, l, loc="upper center",
            bbox_to_anchor=(0.45, -1.2), fontsize=17,
            ncol=3)
    ax.add_artist(l1)

    # vertical lines
    ax.axvline(x=2.5, color='k', linestyle="--", linewidth=2)
    ax.axvline(x=6.5, color='k', linestyle="--", linewidth=2)
    ax.axvline(x=9.5, color='k', linestyle="--", linewidth=2)

    ax.text(0.1, 105, "LRU-favor", fontsize=18)
    ax.text(3.6, 105, "LFU-favor", fontsize=18)
    ax.text(6.6, 105, "Random-favor", fontsize=18)
    ax.text(9.5, 105, "Neut.", fontsize=18)

    # save
    plot_path = "%s/migration_policy_selection_ratio" % (args.result_dir)
    fig.savefig(plot_path + ".png", bbox_inches="tight")
    fig.savefig(plot_path + ".pdf", bbox_inches="tight")
    plt.close()

if __name__ == "__main__":
    main()
