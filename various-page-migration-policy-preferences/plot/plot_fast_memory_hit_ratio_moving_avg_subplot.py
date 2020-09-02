#!/usr/bin/env python3

"""
   plot_fast_memory_hit_ratio_moving_avg_subplot.py

    Created on: Jan. 25, 2019
        Author: Taekyung Heo <tkheo@casys.kaist.ac.kr>
"""

import argparse
import itertools
import matplotlib as mpl
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
from matplotlib.colors import ListedColormap
from matplotlib.lines import Line2D
mpl.use("Agg")
mpl.rcParams["legend.fancybox"] = False
mpl.rcParams["legend.edgecolor"] = "inherit"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-data", required=True)
    parser.add_argument("-result_dir", required=True)
    args = parser.parse_args()

    abbr_workload_name_li = ["cactus", "graph500", "lbm"]

    # load data
    data = {}
    with open(args.data) as f:
        for line in f:
            splitted_line = line.strip().split(",")
            abbr_workload_name = splitted_line[0]
            thp = splitted_line[1]
            mig_policy = splitted_line[2]
            feature_values_li = list(map(float, splitted_line[3:]))

            if abbr_workload_name not in data.keys():
                data.update({abbr_workload_name: {}})
            if ("Modified" not in mig_policy) and ("Random" not in mig_policy):
                data[abbr_workload_name].update({mig_policy: feature_values_li})

    # prepare colors
    colors = []
    cmap = cm.get_cmap("gnuplot")
    for i in range(3):
        colors.append(cmap(i*0.333))
    colors = colors[:-1]

    # subplot
    fig, axs = plt.subplots(1, 3)
    axs = axs.flatten()
    fig.set_size_inches(28, 2.2)

    # adjust subplot margins
    left = 0.04
    right = 0.65
    bottom = 0.05
    top = 0.65
    wspace = 0.15
    hspace = 0.6
    plt.subplots_adjust(left=left, right=right, bottom=bottom, top=top, wspace=wspace, hspace=hspace)

    # plot
    for i, abbr_workload_name in enumerate(abbr_workload_name_li):
        ax = axs[i]
        ax.set_title("%s" % (abbr_workload_name), fontsize=21)
        if i == 0:
            ax.set_ylabel("Fast Mem.\nHit Ratio (%)", fontsize=20)
        if i == 1:
            ax.set_xlabel("Epochs", fontsize=20)
        ax.tick_params(axis="x", labelsize=20)
        ax.tick_params(axis="y", labelsize=20)
        ax.set_ylim(0, 60.00001)
        start, end = ax.get_ylim()
        ax.yaxis.set_ticks(np.arange(start, end, 20))
        ax.grid(linestyle="--", alpha=0.8)

        marker_li = itertools.cycle(("D", "s"))
        ls_li = itertools.cycle(("-", "--"))
        color_li = itertools.cycle(colors)
        for j, mig_policy in enumerate(sorted(data[abbr_workload_name].keys())):
            feature_values_li = data[abbr_workload_name][mig_policy]
            color = next(color_li)
            ax.plot(feature_values_li, linewidth=3, color=color,
                    marker=next(marker_li), markersize=12, markerfacecolor=color, markevery=50,
                    linestyle=next(ls_li),
                    label=mig_policy)

    # add legend
    legend_elements = [
        Line2D([0], [0], marker="s", label="LRU", color=colors[1], markerfacecolor=colors[1], markersize=15, linestyle="--", lw=3),
        Line2D([0], [0], marker="D", label="LFU", color=colors[0], markerfacecolor=colors[0], markersize=15, linestyle="-", lw=3),
    ]
    ax.legend(handles=legend_elements, bbox_to_anchor=(-0.66, -1.15), loc="lower center", ncol=3, fontsize=21)

    plot_path = "%s/migration_policy_fast_memory_hit_ratio_moving_avg_subplot" % (args.result_dir)
    fig.savefig(plot_path + ".png", bbox_inches="tight")
    fig.savefig(plot_path + ".pdf", bbox_inches="tight")
    plt.close()

if __name__ == "__main__":
    main()
